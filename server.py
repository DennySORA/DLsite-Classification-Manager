# mypy: ignore-errors

import argparse
import logging
import os
import re
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from dlsite_classification.common.security import (
    PathSecurityError,
    validate_path_within_root,
)
from dlsite_classification.extract.extract import ExtractFolder
from dlsite_classification.tools.url import build_image_url, decode_url_path


app = FastAPI(title="DLsite Collection Manager", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_data_path():
    """獲取數據路徑，優先級：命令行參數 > 環境變數 > 預設值"""
    # 1. 檢查命令行參數
    parser = argparse.ArgumentParser(description="DLsite Collection Manager API Server")
    parser.add_argument(
        "--data-path", "-d", help="Path to DLsite collection data directory"
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8001,
        help="Port to run the server on (default: 8001)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind the server to (default: 0.0.0.0)",
    )

    # 只解析已知的參數，避免與 uvicorn 的參數衝突
    args, unknown = parser.parse_known_args()

    if args.data_path:
        return args.data_path, args.port, args.host

    # 2. 檢查環境變數
    env_path = os.getenv("DLSITE_DATA_PATH")
    if env_path:
        return env_path, args.port, args.host

    # 3. 使用預設值
    default_paths = [
        "./test_game_info",  # 測試數據
        "/mnt/d/R18/DLsite",  # 原始預設路徑
        "./data",  # 通用數據路徑
    ]

    for path in default_paths:
        if os.path.exists(path):
            return path, args.port, args.host

    # 如果都不存在，使用第一個作為預設值
    return default_paths[0], args.port, args.host


# 獲取數據路徑和伺服器配置
DATA_PATH, SERVER_PORT, SERVER_HOST = get_data_path()
extract_data = ExtractFolder(DATA_PATH)

print(f"🗂️  Data path: {DATA_PATH}")
print(f"🌐 Server will run on: http://{SERVER_HOST}:{SERVER_PORT}")


# 標準化和去重函數
def normalize_and_deduplicate_list(items):
    """標準化和去重列表項目"""
    if not items:
        return []

    normalized_items = set()
    for item in items:
        if item and isinstance(item, str):
            # 移除前後空格和特殊字符
            cleaned = item.strip().strip("/")
            if cleaned:
                # 移除多餘的空格和末尾空格
                cleaned = re.sub(r"\s+", " ", cleaned).strip()
                # 移除重複的空格標記（如 "ロリ " -> "ロリ"）
                if cleaned not in [existing.strip() for existing in normalized_items]:
                    normalized_items.add(cleaned)

    return sorted(list(normalized_items))


def smart_merge_similar_items(items):
    """智能合併相似項目"""
    if not items:
        return []

    merged = {}
    for item in items:
        # 標準化項目
        base_item = item.strip().rstrip(" ")

        # 檢查是否有相似項目已存在
        found_similar = False
        for existing_key in list(merged.keys()):
            # 如果完全匹配或只差空格，合併
            if (
                base_item == existing_key
                or base_item.replace(" ", "") == existing_key.replace(" ", "")
                or base_item == existing_key.rstrip(" ")
                or base_item.rstrip(" ") == existing_key
            ):
                merged[existing_key] += 1
                found_similar = True
                break

        if not found_similar:
            merged[base_item] = 1

    return [
        {"name": k, "count": v}
        for k, v in sorted(merged.items(), key=lambda x: x[1], reverse=True)
    ]


def split_and_normalize_formats(format_string):
    """分割並標準化作品形式字串"""
    if not format_string or not isinstance(format_string, str):
        return []

    # 移除開頭的 "/"
    cleaned = format_string.strip().lstrip("/")
    if not cleaned:
        return []

    # 分割多個格式 (以 / 或 , 分隔)
    parts = re.split(r"[/,]", cleaned)

    normalized_parts = []
    for part in parts:
        part = part.strip()
        if part and part not in ["", "/"]:
            # 標準化常見格式
            if "音声あり" in part and "音楽あり" in part and "動画あり" in part:
                base = (
                    part.replace("音声あり", "")
                    .replace("音楽あり", "")
                    .replace("動画あり", "")
                    .strip()
                )
                if base:
                    normalized_parts.append(base)
                    normalized_parts.append("音声あり")
                    normalized_parts.append("音楽あり")
                    normalized_parts.append("動画あり")
            elif "音声あり" in part and "音楽あり" in part:
                base = part.replace("音声あり", "").replace("音楽あり", "").strip()
                if base:
                    normalized_parts.append(base)
                    normalized_parts.append("音声あり")
                    normalized_parts.append("音楽あり")
            elif "音声あり" in part and "動画あり" in part:
                base = part.replace("音声あり", "").replace("動画あり", "").strip()
                if base:
                    normalized_parts.append(base)
                    normalized_parts.append("音声あり")
                    normalized_parts.append("動画あり")
            elif "音楽あり" in part and "動画あり" in part:
                base = part.replace("音楽あり", "").replace("動画あり", "").strip()
                if base:
                    normalized_parts.append(base)
                    normalized_parts.append("音楽あり")
                    normalized_parts.append("動画あり")
            elif "音声あり" in part:
                base = part.replace("音声あり", "").strip()
                if base:
                    normalized_parts.append(base)
                    normalized_parts.append("音声あり")
            elif "音楽あり" in part:
                base = part.replace("音楽あり", "").strip()
                if base:
                    normalized_parts.append(base)
                    normalized_parts.append("音楽あり")
            elif "動画あり" in part:
                base = part.replace("動画あり", "").strip()
                if base:
                    normalized_parts.append(base)
                    normalized_parts.append("動画あり")
            else:
                normalized_parts.append(part)

    return normalize_and_deduplicate_list(normalized_parts)


class WorkResponse(BaseModel):
    code: str
    title: str
    company: str
    genre: list[str]
    image_url: str
    sample_images: list[str]
    introduction: str
    sale_date: str | None
    work_format: list[str]
    age_rating: list[str]
    file_size: list[str]
    my_rating: str | None = None
    my_collection: str | None = None
    my_collections: list[str] | None = None


class CompanyResponse(BaseModel):
    name: str
    work_count: int
    works: list[WorkResponse]


class SearchResponse(BaseModel):
    total: int
    works: list[WorkResponse]
    companies: list[str]
    genres: list[str]


# Helper function to convert work data
def convert_work_to_response(work: Any, work_folder: str) -> WorkResponse:
    try:
        if not work.info or not work.info.tag:
            return None

        tag = work.info.tag

        # Extract title
        title = work.name
        if tag.title and isinstance(tag.title, dict):
            title = list(tag.title.keys())[0] if tag.title else work.name

        # Extract company
        company = "Unknown"
        if tag.company and isinstance(tag.company, dict):
            company = list(tag.company.keys())[0]

        # Extract genres and deduplicate
        genre = []
        if tag.genre and isinstance(tag.genre, dict):
            # Remove duplicates while preserving order and filtering empty values
            seen = set()
            for g in tag.genre:
                if g and g.strip():  # Filter out empty or whitespace-only strings
                    g_cleaned = g.strip()
                    g_lower = g_cleaned.lower()
                    if g_lower not in seen:
                        seen.add(g_lower)
                        genre.append(g_cleaned)

        # Extract work format with smart splitting and normalization
        work_format = []
        if tag.work_format and isinstance(tag.work_format, dict):
            for format_str in tag.work_format:
                work_format.extend(split_and_normalize_formats(format_str))
            work_format = normalize_and_deduplicate_list(work_format)

        # Extract age rating
        age_rating = []
        if tag.age and isinstance(tag.age, dict):
            age_rating = list(tag.age.keys())

        # Extract file size (keeping original for size info)
        file_size = []
        if tag.file_capacity and isinstance(tag.file_capacity, dict):
            file_size = normalize_and_deduplicate_list(list(tag.file_capacity.keys()))

        # Extract sale date
        sale_date = None
        if tag.sale_date and isinstance(tag.sale_date, dict):
            sale_date = list(tag.sale_date.keys())[0] if tag.sale_date else None

        # Extract user rating
        my_rating = None
        if hasattr(tag, "my_rating") and tag.my_rating:
            my_rating = tag.my_rating

        # Extract user collection
        my_collection = None
        if hasattr(tag, "my_collection") and tag.my_collection:
            my_collection = tag.my_collection

        # Extract user collections (multiple)
        my_collections = None
        if hasattr(tag, "my_collections") and tag.my_collections:
            my_collections = tag.my_collections

        # Get main image
        main_image = None
        sample_images = []
        if work.info.images:
            for img in work.info.images:
                if "img_main" in img:
                    main_image = build_image_url(os.path.join(work.info.path, img))
                elif "img_smp" in img:
                    sample_images.append(
                        build_image_url(os.path.join(work.info.path, img))
                    )

            if not main_image and work.info.images:
                main_image = build_image_url(
                    os.path.join(work.info.path, work.info.images[0])
                )

        return WorkResponse(
            code=work.code,
            title=title,
            company=company,
            genre=genre,
            image_url=main_image or "",
            sample_images=sample_images,
            introduction=tag.introduction or "",
            sale_date=sale_date,
            work_format=work_format,
            age_rating=age_rating,
            file_size=file_size,
            my_rating=my_rating,
            my_collection=my_collection,
            my_collections=my_collections,
        )
    except Exception as e:
        logging.exception(
            "Error converting work to response for folder %s: %s", work_folder, e
        )
        return None


@app.get("/")
async def root():
    return {"message": "DLsite Collection Manager API"}


@app.get("/status")
async def status():
    """Check API status and data loading"""
    if not extract_data.classification_table:
        try:
            await extract_data.scan_file()
        except Exception as e:
            return {"status": "error", "message": f"Failed to scan files: {e}"}

    total_companies = len(extract_data.classification_table)
    total_works = sum(
        len(company.work_item) for company in extract_data.classification_table.values()
    )

    return {
        "status": "ok",
        "total_companies": total_companies,
        "total_works": total_works,
        "data_path": DATA_PATH,
    }


@app.get("/works", response_model=SearchResponse)
async def get_works(
    search: str | None = Query(None, description="Search in title, company, genre"),
    company: str | None = Query(None, description="Filter by company"),
    collection: str | None = Query(None, description="Filter by collection"),
    rating: str | None = Query(None, description="Filter by rating"),
    tags: str | None = Query(None, description="Filter by tags (comma-separated)"),
    tag_mode: str = Query("OR", description="Tag filter mode: OR or AND"),
    work_format: str | None = Query(None, description="Filter by work format"),
    file_format: str | None = Query(None, description="Filter by file format"),
    sort: str = Query(
        "title", description="Sort by: title, sale_date, company, rating, collection"
    ),
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    # Ensure data is scanned
    if not extract_data.classification_table:
        await extract_data.scan_file()

    all_works = []
    all_companies = set()
    all_genres = set()

    # Process all companies and works
    for company_folder, company_data in extract_data.classification_table.items():
        # Extract company name from the first work's company.tag instead of folder name
        company_display_name = company_folder
        if company_data.work_item:
            first_work = next(iter(company_data.work_item.values()))
            if first_work.info and first_work.info.tag and first_work.info.tag.company:
                company_name_from_tag = list(first_work.info.tag.company.keys())[0]
                company_display_name = company_name_from_tag

        all_companies.add(company_display_name)

        for work_folder, work in company_data.work_item.items():
            work_response = convert_work_to_response(work, work_folder)
            if work_response:
                # Fix company name display
                work_response.company = company_display_name
                all_works.append(work_response)
                # Add genres to global collection for statistics
                for genre in work_response.genre:
                    if genre and genre.strip():
                        all_genres.add(genre.strip())

    # Apply filters
    filtered_works = all_works

    # Text search
    if search:
        search_lower = search.lower()
        filtered_works = [
            work
            for work in filtered_works
            if (
                search_lower in work.title.lower()
                or search_lower in work.company.lower()
                or search_lower in work.code.lower()
                or search_lower in work.introduction.lower()
                or any(search_lower in genre.lower() for genre in work.genre)
            )
        ]

    # Company filter
    if company:
        filtered_works = [
            work for work in filtered_works if company.lower() in work.company.lower()
        ]

    # Collection filter
    if collection:
        filtered_works = [
            work
            for work in filtered_works
            if (work.my_collection and collection.lower() in work.my_collection.lower())
            or (
                hasattr(work, "my_collections")
                and work.my_collections
                and any(collection.lower() in c.lower() for c in work.my_collections)
            )
        ]

    # Rating filter
    if rating:
        min_rating = int(rating)
        filtered_works = [
            work
            for work in filtered_works
            if work.my_rating and int(work.my_rating) >= min_rating
        ]

    # Tag filter with OR/AND logic
    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        if tag_mode.upper() == "AND":
            # AND mode: work must have ALL selected tags
            filtered_works = [
                work
                for work in filtered_works
                if all(
                    any(tag in genre.lower() for genre in work.genre)
                    for tag in tag_list
                )
            ]
        else:
            # OR mode: work must have ANY of the selected tags
            filtered_works = [
                work
                for work in filtered_works
                if any(
                    any(tag in genre.lower() for genre in work.genre)
                    for tag in tag_list
                )
            ]

    # Work format filter
    if work_format:
        filtered_works = [
            work
            for work in filtered_works
            if any(work_format.lower() in wf.lower() for wf in work.work_format)
        ]

    # File format filter
    if file_format:
        filtered_works = [
            work
            for work in filtered_works
            if any(file_format.lower() in ff.lower() for ff in work.file_size)
        ]

    # Sorting with safe rating conversion
    def safe_rating(w: WorkResponse) -> int:
        try:
            return int(w.my_rating) if w.my_rating is not None else 0
        except (ValueError, TypeError):
            return 0

    if sort == "sale_date":
        filtered_works.sort(key=lambda x: x.sale_date or "", reverse=True)
    elif sort == "company":
        filtered_works.sort(key=lambda x: x.company.lower())
    elif sort == "rating":
        filtered_works.sort(key=safe_rating, reverse=True)
    elif sort == "collection":
        filtered_works.sort(key=lambda x: x.my_collection or "")
    else:  # title
        filtered_works.sort(key=lambda x: x.title.lower())

    # Pagination
    total = len(filtered_works)
    paginated_works = filtered_works[offset : offset + limit]

    return SearchResponse(
        total=total,
        works=paginated_works,
        companies=sorted(list(all_companies)),
        genres=sorted(list(all_genres)),
    )


@app.get("/companies", response_model=list[CompanyResponse])
async def get_companies():
    if not extract_data.classification_table:
        await extract_data.scan_file()

    companies = []
    for company_name, company_data in extract_data.classification_table.items():
        works = []
        for work_folder, work in company_data.work_item.items():
            work_response = convert_work_to_response(work, work_folder)
            if work_response:
                works.append(work_response)

        if works:
            # Get company display name from first work's tag
            company_display_name = company_name
            if works:
                company_display_name = works[0].company

            companies.append(
                CompanyResponse(
                    name=company_display_name, work_count=len(works), works=works
                )
            )

    return sorted(companies, key=lambda x: x.work_count, reverse=True)


@app.get("/work/{code}")
async def get_work_detail(code: str):
    if not extract_data.classification_table:
        await extract_data.scan_file()

    for _company_name, company_data in extract_data.classification_table.items():
        for work_folder, work in company_data.work_item.items():
            if work.code == code:
                work_response = convert_work_to_response(work, work_folder)
                if work_response:
                    # Add additional detail information
                    tag = work.info.tag
                    additional_info = {
                        "series": list(tag.series.keys()) if tag.series else [],
                        "voice_actor": list(tag.voice_actor.keys())
                        if tag.voice_actor
                        else [],
                        "author": list(tag.author.keys()) if tag.author else [],
                        "illustration": list(tag.illustration.keys())
                        if tag.illustration
                        else [],
                        "scenario": list(tag.scenario.keys()) if tag.scenario else [],
                        "music": list(tag.music.keys()) if tag.music else [],
                        "file_format": list(tag.file_format.keys())
                        if tag.file_format
                        else [],
                        "operating_environment": list(tag.operating_environment.keys())
                        if tag.operating_environment
                        else [],
                        "update_date": list(tag.update_date.keys())
                        if tag.update_date
                        else [],
                        "star": tag.star if tag.star else None,
                        "pages": list(tag.pages.keys()) if tag.pages else [],
                        "event": list(tag.event.keys()) if tag.event else [],
                        "other": list(tag.other.keys()) if tag.other else [],
                        "languages": list(tag.languages.keys())
                        if tag.languages
                        else [],
                    }
                    return {**work_response.dict(), **additional_info}

    raise HTTPException(status_code=404, detail="Work not found")


@app.get("/genres")
async def get_all_genres():
    if not extract_data.classification_table:
        await extract_data.scan_file()

    genre_counts = {}
    for _company_name, company_data in extract_data.classification_table.items():
        for _work_folder, work in company_data.work_item.items():
            if work.info and work.info.tag and work.info.tag.genre:
                for genre in work.info.tag.genre:
                    if genre and genre.strip():
                        normalized_genre = genre.strip()
                        if normalized_genre in genre_counts:
                            genre_counts[normalized_genre] += 1
                        else:
                            genre_counts[normalized_genre] = 1

    # 創建包含計數的標籤列表，按使用頻率排序
    genres_with_counts = [
        {"name": genre, "count": count}
        for genre, count in genre_counts.items()
        if count > 0  # 只包含有計數的標籤
    ]

    # 按使用頻率排序（從高到低）
    genres_with_counts.sort(key=lambda x: x["count"], reverse=True)

    return {"genres": genres_with_counts}


@app.get("/work-formats")
async def get_all_work_formats():
    if not extract_data.classification_table:
        await extract_data.scan_file()

    all_work_formats = set()
    for _, company_data in extract_data.classification_table.items():
        for _, work in company_data.work_item.items():
            if work.info and work.info.tag and work.info.tag.work_format:
                for format_str in work.info.tag.work_format:
                    normalized_formats = split_and_normalize_formats(format_str)
                    all_work_formats.update(normalized_formats)

    return {"work_formats": sorted(list(all_work_formats))}


@app.get("/file-formats")
async def get_all_file_formats():
    if not extract_data.classification_table:
        await extract_data.scan_file()

    all_file_formats = set()
    for _, company_data in extract_data.classification_table.items():
        for _, work in company_data.work_item.items():
            if work.info and work.info.tag and work.info.tag.file_format:
                for format_str in work.info.tag.file_format:
                    normalized_formats = split_and_normalize_formats(format_str)
                    all_file_formats.update(normalized_formats)

    return {"file_formats": sorted(list(all_file_formats))}


class UserDataRequest(BaseModel):
    rating: str | None = None
    collection: str | None = None
    collections: list[str] | None = None


@app.post("/work/{code}/user-data")
async def update_user_data(code: str, user_data: UserDataRequest):
    """Update user's rating and collection for a work"""
    if not extract_data.classification_table:
        await extract_data.scan_file()

    # Find the work
    for _, company_data in extract_data.classification_table.items():
        for _, work in company_data.work_item.items():
            if work.code == code:
                if not work.info or not work.info.path:
                    raise HTTPException(status_code=404, detail="Work info not found")

                info_path = work.info.path

                # Save rating
                if user_data.rating is not None:
                    rating_file = os.path.join(info_path, "my_rating.tag")
                    try:
                        with open(rating_file, "w", encoding="utf-8") as f:
                            f.write(user_data.rating)
                        # Update in-memory data immediately without full rescan
                        if work.info.tag:
                            work.info.tag.my_rating = user_data.rating
                    except Exception as e:
                        raise HTTPException(
                            status_code=500, detail=f"Failed to save rating: {e}"
                        ) from e

                # Save single collection (backward compatibility)
                if user_data.collection is not None:
                    collection_file = os.path.join(info_path, "my_collection.tag")
                    try:
                        with open(collection_file, "w", encoding="utf-8") as f:
                            f.write(user_data.collection)
                        # Update in-memory data immediately
                        if work.info.tag:
                            work.info.tag.my_collection = user_data.collection
                    except Exception as e:
                        raise HTTPException(
                            status_code=500, detail=f"Failed to save collection: {e}"
                        ) from e

                # Save multiple collections
                if user_data.collections is not None:
                    collections_file = os.path.join(info_path, "my_collections.tag")
                    try:
                        with open(collections_file, "w", encoding="utf-8") as f:
                            for collection in user_data.collections:
                                f.write(f"{collection}\n")
                        # Update in-memory data immediately
                        if work.info.tag:
                            work.info.tag.my_collections = user_data.collections
                    except Exception as e:
                        raise HTTPException(
                            status_code=500, detail=f"Failed to save collections: {e}"
                        ) from e

                    # Also update single collection for backward compatibility
                    if user_data.collections:
                        collection_file = os.path.join(info_path, "my_collection.tag")
                        try:
                            with open(collection_file, "w", encoding="utf-8") as f:
                                f.write(user_data.collections[0])
                            # Update in-memory data immediately
                            if work.info.tag:
                                work.info.tag.my_collection = user_data.collections[0]
                        except Exception as e:
                            logging.warning(
                                "Failed to save backward compatible collection for %s: %s",
                                code,
                                e,
                            )

                # No need to refresh all data - we've updated in-memory
                # await extract_data.scan_file()

                return {"status": "success", "message": "User data updated"}

    raise HTTPException(status_code=404, detail="Work not found")


@app.get("/collections")
async def get_collections():
    """Get all unique collection categories"""
    if not extract_data.classification_table:
        await extract_data.scan_file()

    collections = set()
    for _, company_data in extract_data.classification_table.items():
        for _, work in company_data.work_item.items():
            if work.info and work.info.tag:
                # Add single collection
                if work.info.tag.my_collection:
                    collections.add(work.info.tag.my_collection)
                # Add multiple collections
                if (
                    hasattr(work.info.tag, "my_collections")
                    and work.info.tag.my_collections
                ):
                    for collection in work.info.tag.my_collections:
                        collections.add(collection)

    return {"collections": sorted(list(collections))}


@app.get("/image")
async def get_image(path: str):
    """Serve image files with URL decoding and security validation.

    Decodes URL-encoded paths and validates that the requested file
    is within the allowed data directory to prevent directory traversal attacks.

    Args:
        path: URL-encoded absolute path to the image file

    Returns:
        FileResponse with the requested image

    Raises:
        HTTPException 403: If path is outside allowed directory
        HTTPException 404: If image file not found
    """
    # Decode URL-encoded path
    decoded_path = decode_url_path(path)

    # Security validation using common security module
    try:
        validated_path = validate_path_within_root(
            decoded_path, DATA_PATH, check_exists=True
        )
    except PathSecurityError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return FileResponse(validated_path)


@app.get("/scan")
async def scan():
    use_time = await extract_data.scan_file()
    return {
        "status": "ok",
        "scan_time": use_time,
        "total_works": len(
            [
                work
                for company in extract_data.classification_table.values()
                for work in company.work_item.values()
            ]
        ),
    }


if __name__ == "__main__":
    # 檢查數據路徑是否存在
    if not os.path.exists(DATA_PATH):
        print(f"⚠️  Warning: Data path '{DATA_PATH}' does not exist!")
        print("📁 You can specify a custom path using:")
        print("   python server.py --data-path /path/to/your/data")
        print(
            "   or set environment variable: export DLSITE_DATA_PATH=/path/to/your/data"
        )
        print(
            "🚀 Server will start anyway, but scanning will fail until the path exists."
        )
        print()

    uvicorn.run("server:app", host=SERVER_HOST, port=SERVER_PORT, log_level="info")
