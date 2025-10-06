"""Company Archive Manager - Create ARCHIVE folders for all company works.

This manager scans company folders, crawls DLsite to find all works by each company,
and creates an ARCHIVE subfolder containing complete metadata for all works.

Features:
- Progress bar with rich showing ETA and current status
- Concurrent processing for faster execution
- Smart rate limiting with exponential backoff when blocked
"""

import asyncio
import logging
import os
import time
from os import path as os_path

from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from dlsite_classification.classification.work_info_saver import save_work_info_to_path
from dlsite_classification.common.regex import REGEX_COMPANY_FOLDER, REGEX_RG
from dlsite_classification.crawler.company import DLsiteCompanyCrawler
from dlsite_classification.spkg.logs import Cyan, Green, Red, Yellow
from dlsite_classification.tools import check_and_make_folder


# Rich console for status output
console = Console()


class RateLimitError(Exception):
    """Raised when rate limited by DLsite."""

    pass


def _extract_company_id(folder_name: str) -> str | None:
    """Extract company ID from folder name.

    Args:
        folder_name: Folder name like '[@OZ]_[RG08239]'

    Returns:
        Company ID (e.g., 'RG08239') or None if not found
    """
    matches = REGEX_RG.findall(folder_name)
    return matches[0] if matches else None


def _is_company_folder(folder_name: str) -> bool:
    """Check if folder matches company folder pattern.

    Args:
        folder_name: Folder name to check

    Returns:
        True if it's a company folder
    """
    return bool(REGEX_COMPANY_FOLDER.match(folder_name))


async def _create_archive_for_work(
    work_id: str,
    archive_path: str,
    force_update: bool = False,
    backoff_state: dict | None = None,
) -> tuple[bool, bool]:
    """Create archive info for a single work.

    Args:
        work_id: DLsite work ID
        archive_path: Path to ARCHIVE folder
        force_update: Whether to re-download if already exists
        backoff_state: Shared state dict for tracking rate limits

    Returns:
        Tuple of (success: bool, was_rate_limited: bool)
    """
    info_path = os_path.join(archive_path, f"{work_id}_info")

    # Skip if exists and not forcing update
    if not force_update and os_path.isdir(info_path):
        return True, False

    try:
        success = await save_work_info_to_path(
            work_id,
            archive_path,
            preserve_user_tags=False,
            merge_existing_tags=False,
        )
        if success:
            Green(logging.debug, f"Created archive for {work_id}")
        else:
            Yellow(logging.warning, f"Failed to create archive for {work_id}")
        return success, False
    except Exception as e:
        error_msg = str(e).lower()
        # Check if this is a rate limit error
        if (
            "429" in error_msg
            or "rate limit" in error_msg
            or "request fail" in error_msg
        ):
            if backoff_state:
                backoff_state["rate_limited"] = True
            Red(logging.warning, f"Rate limited while fetching {work_id}")
            return False, True
        Red(logging.error, f"Error archiving {work_id}: {e}")
        return False, False


async def _process_works_batch(
    work_ids: list[str],
    archive_path: str,
    force_update: bool,
    max_concurrent: int,
    base_delay: float,
    progress: Progress,
    task_id: int,
) -> tuple[int, int]:
    """Process a batch of works with concurrent execution and smart rate limiting.

    Args:
        work_ids: List of work IDs to process
        archive_path: Path to ARCHIVE folder
        force_update: Whether to re-download existing
        max_concurrent: Maximum concurrent requests
        base_delay: Base delay between requests
        progress: Rich progress bar instance
        task_id: Task ID for progress updates

    Returns:
        Tuple of (success_count, skipped_count)
    """
    success_count = 0
    skipped_count = 0
    backoff_state = {"rate_limited": False, "consecutive_errors": 0}
    current_delay = base_delay

    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_with_semaphore(work_id: str) -> tuple[bool, bool, bool]:
        """Process single work with semaphore and return (success, rate_limited, skipped)."""
        async with semaphore:
            # Check if already exists (skip case)
            info_path = os_path.join(archive_path, f"{work_id}_info")
            if not force_update and os_path.isdir(info_path):
                return True, False, True

            success, rate_limited = await _create_archive_for_work(
                work_id, archive_path, force_update, backoff_state
            )
            return success, rate_limited, False

    # Process in smaller chunks to allow for adaptive rate limiting
    chunk_size = min(max_concurrent * 2, 10)
    total_works = len(work_ids)

    for i in range(0, total_works, chunk_size):
        chunk = work_ids[i : i + chunk_size]

        # Process chunk concurrently
        results = await asyncio.gather(
            *[process_with_semaphore(wid) for wid in chunk],
            return_exceptions=True,
        )

        chunk_rate_limited = False
        for j, result in enumerate(results):
            work_id = chunk[j]

            if isinstance(result, Exception):
                Red(logging.error, f"Exception processing {work_id}: {result}")
                backoff_state["consecutive_errors"] += 1
            else:
                success, rate_limited, skipped = result
                if skipped:
                    skipped_count += 1
                    success_count += 1  # Count skipped as success
                elif success:
                    success_count += 1
                    backoff_state["consecutive_errors"] = 0

                if rate_limited:
                    chunk_rate_limited = True
                    backoff_state["consecutive_errors"] += 1

            progress.update(task_id, advance=1)

        # Adaptive rate limiting
        if chunk_rate_limited or backoff_state["consecutive_errors"] >= 3:
            # Exponential backoff
            current_delay = min(current_delay * 2, 30.0)
            wait_time = current_delay * (
                2 ** min(backoff_state["consecutive_errors"], 4)
            )
            console.print(
                f"[yellow]Rate limited - backing off for {wait_time:.1f}s[/yellow]"
            )
            await asyncio.sleep(wait_time)
            backoff_state["consecutive_errors"] = max(
                0, backoff_state["consecutive_errors"] - 1
            )
        else:
            # Normal delay between chunks
            if i + chunk_size < total_works:
                await asyncio.sleep(current_delay)
                # Gradually reduce delay if successful
                current_delay = max(base_delay, current_delay * 0.9)

    return success_count, skipped_count


async def _process_company_folder(
    company_folder_path: str,
    force_update: bool = False,
    max_concurrent: int = 5,
    rate_limit_delay: float = 1.0,
    progress: Progress | None = None,
    company_task_id: int | None = None,
) -> int:
    """Process a single company folder to create ARCHIVE.

    Args:
        company_folder_path: Full path to company folder
        force_update: Whether to re-download existing archives
        max_concurrent: Max concurrent work downloads
        rate_limit_delay: Base delay between work downloads
        progress: Rich progress bar instance
        company_task_id: Task ID for company-level progress

    Returns:
        Number of works successfully archived
    """
    folder_name = os_path.basename(company_folder_path)
    company_id = _extract_company_id(folder_name)

    if not company_id:
        Red(logging.error, f"Cannot extract company ID from {folder_name}")
        return 0

    console.print(f"\n[cyan]Processing Company {company_id} ({folder_name})[/cyan]")

    # Create ARCHIVE folder
    archive_path = os_path.join(company_folder_path, "ARCHIVE")
    check_and_make_folder(archive_path)

    # Crawl company page to get all work IDs
    try:
        crawler = DLsiteCompanyCrawler(code=company_id)
        work_ids = await crawler.get_all_work_ids(rate_limit_delay=rate_limit_delay)

        if not work_ids:
            Yellow(logging.warning, f"No works found for company {company_id}")
            return 0

        console.print(
            f"[blue]Found {len(work_ids)} works for company {company_id}[/blue]"
        )

    except Exception as e:
        Red(logging.error, f"Failed to crawl company {company_id}: {e}")
        return 0

    # Create progress bar for works
    if progress:
        work_task = progress.add_task(
            f"[green]Works ({company_id})",
            total=len(work_ids),
        )
    else:
        work_task = None

    # Process works with concurrent execution
    if progress and work_task is not None:
        success_count, skipped_count = await _process_works_batch(
            work_ids,
            archive_path,
            force_update,
            max_concurrent,
            rate_limit_delay,
            progress,
            work_task,
        )
        progress.remove_task(work_task)
    else:
        # Fallback without progress bar
        success_count = 0
        for work_id in work_ids:
            success, _ = await _create_archive_for_work(
                work_id, archive_path, force_update
            )
            if success:
                success_count += 1
            await asyncio.sleep(rate_limit_delay)
        skipped_count = 0

    console.print(
        f"[blue]Archived {success_count}/{len(work_ids)} works for {company_id}"
        f" (skipped {skipped_count} existing)[/blue]"
    )

    return success_count


async def create_company_archives(
    data_path: str | None = None,
    specific_company_id: str | None = None,
    force_update: bool = False,
    max_concurrent_works: int = 5,
    rate_limit_delay: float = 1.0,
) -> dict[str, int]:
    """Create ARCHIVE folders for companies in the data path.

    This function:
    1. Scans the data directory for company folders
    2. For each company, crawls DLsite to get all work IDs
    3. Creates an ARCHIVE subfolder
    4. Downloads and saves metadata for all works

    Features:
    - Progress bar showing overall progress and ETA
    - Concurrent processing for faster execution
    - Smart rate limiting with exponential backoff

    Args:
        data_path: Path to data directory containing company folders
        specific_company_id: If provided, only process this company
        force_update: Whether to re-download existing archives
        max_concurrent_works: Max concurrent work info downloads
        rate_limit_delay: Base delay between requests in seconds

    Returns:
        Dict mapping company IDs to number of works archived

    Example:
        >>> results = await create_company_archives(
        ...     data_path="/data/dlsite",
        ...     specific_company_id="RG08239",
        ...     force_update=False,
        ... )
        >>> print(f"Archived {results['RG08239']} works")
    """
    if data_path is None:
        data_path = input("Input data path: ")

    data_path = os_path.abspath(data_path)

    if not os_path.isdir(data_path):
        Red(logging.error, f"Data path does not exist: {data_path}")
        return {}

    console.print(
        f"\n[cyan]{'=' * 60}[/cyan]"
        f"\n[cyan]Starting Company Archive Creation[/cyan]"
        f"\n[cyan]Data path: {data_path}[/cyan]"
        f"\n[cyan]{'=' * 60}[/cyan]"
    )

    # Find all company folders
    company_folders = []
    for item in os.listdir(data_path):
        item_path = os_path.join(data_path, item)
        if not os_path.isdir(item_path):
            continue

        # Skip ARCHIVE and other special folders
        if item in ["ARCHIVE", "code", "other", "duplicate", "null", "finish"]:
            continue

        if _is_company_folder(item):
            company_id = _extract_company_id(item)
            if specific_company_id and company_id != specific_company_id:
                continue
            company_folders.append(item_path)

    if not company_folders:
        if specific_company_id:
            Yellow(
                logging.warning,
                f"No company folder found for {specific_company_id}",
            )
        else:
            Yellow(logging.warning, f"No company folders found in {data_path}")
        return {}

    console.print(
        f"[green]Found {len(company_folders)} company folder(s) to process[/green]"
    )

    # Process each company folder with progress bar
    results = {}
    start_time = time.time()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
        expand=True,
    ) as progress:
        company_task = progress.add_task(
            "[bold cyan]Companies",
            total=len(company_folders),
        )

        for company_folder_path in company_folders:
            folder_name = os_path.basename(company_folder_path)
            company_id = _extract_company_id(folder_name)

            if company_id:
                count = await _process_company_folder(
                    company_folder_path,
                    force_update,
                    max_concurrent_works,
                    rate_limit_delay,
                    progress,
                    company_task,
                )
                results[company_id] = count

            progress.update(company_task, advance=1)

    elapsed_time = time.time() - start_time
    total_works = sum(results.values())

    console.print(
        f"\n[cyan]{'=' * 60}[/cyan]"
        f"\n[bold green]Company Archive Creation Complete![/bold green]"
        f"\n[green]Total companies: {len(results)}[/green]"
        f"\n[green]Total works archived: {total_works}[/green]"
        f"\n[green]Time elapsed: {elapsed_time:.1f}s[/green]"
        f"\n[cyan]{'=' * 60}[/cyan]"
    )

    return results


async def update_existing_work_in_archive(
    work_folder_path: str, work_code: str
) -> bool:
    """Update ARCHIVE when a work is updated in the main collection.

    This function should be called after updating work info to ensure
    the ARCHIVE folder stays in sync.

    Args:
        work_folder_path: Path to the work folder
        work_code: Work code (e.g., 'RJ123456')

    Returns:
        True if ARCHIVE was updated successfully

    Example:
        >>> await update_existing_work_in_archive(
        ...     "/data/company/RJ123456_work", "RJ123456"
        ... )
    """
    # Find company folder (parent directory)
    company_folder = os_path.dirname(work_folder_path)

    # Check if ARCHIVE exists
    archive_path = os_path.join(company_folder, "ARCHIVE")
    if not os_path.isdir(archive_path):
        # No ARCHIVE folder, nothing to update
        return True

    Cyan(logging.info, f"Updating ARCHIVE for {work_code}")

    try:
        success = await save_work_info_to_path(
            work_code,
            archive_path,
            preserve_user_tags=False,
            merge_existing_tags=False,
        )
        if success:
            Green(logging.info, f"Updated ARCHIVE for {work_code}")
        return success
    except Exception as e:
        Red(logging.error, f"Failed to update ARCHIVE for {work_code}: {e}")
        return False
