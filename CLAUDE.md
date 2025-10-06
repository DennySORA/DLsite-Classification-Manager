# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DLsite Classification Manager is a high-performance DLsite works classification and management tool with a modern web interface and complete API functionality. It automatically extracts and manages metadata for DLsite content (identified by codes: RJ, BJ, VJ, RE, BE, VE).

## Running Unit Tests

**IMPORTANT: Always run tests using the standardized script to ensure consistent results.**

To verify unit tests after any code changes:

```bash
./run_tests.sh
```

This script ensures:
- ✅ Tests are run with correct coverage settings
- ✅ Only tested modules are measured (100% coverage for URL and security modules)
- ✅ Consistent results between all developers
- ✅ Fast execution (~0.4 seconds for 81 tests)

**Note**: If you see "bad interpreter" error on WSL/Linux, the file may have Windows line endings. Fix with:
```bash
sed -i 's/\r$//' run_tests.sh && chmod +x run_tests.sh
```

For detailed testing documentation, see [TESTING.md](TESTING.md).

## Architectural Philosophy & Design Principles

### Core Architecture Design

This codebase follows a **layered separation of concerns** architecture with clear boundaries:

1. **Presentation Layer** (CLI/API)
   - `main.py`: CLI entry point
   - `server.py`: FastAPI REST API
   - Both delegate to manager layer, never directly touching data/business logic

2. **Manager Layer** (Workflow Orchestration)
   - `manager/`: Coordinates workflows between classification, crawler, and extract layers
   - Acts as façade pattern - simplifies complex subsystem interactions
   - Examples: `manager_auto_classificatiom.py`, `manager_work_update.py`

3. **Business Logic Layer**
   - `classification/`: Domain logic for folder organization and categorization
   - `crawler/`: Data acquisition from external DLsite sources
   - `extract/`: File system data extraction and parsing

4. **Data Layer**
   - `extract/structure.py`: Domain models (Pydantic-based)
   - File system as persistent storage (`.tag` files)

5. **Infrastructure Layer**
   - `tools/`: Pure utility functions (file I/O, search, move operations)
   - `common/`: Shared constants and helpers (regex, networking)
   - `spkg/`: Support packages (async runners, logging)

### Why This Separation?

**Dependency Direction**: Dependencies flow inward (manager → business logic → data models). Outer layers depend on inner layers, never vice versa. This creates:
- **Testability**: Can test business logic without file system or network
- **Flexibility**: Can swap CLI for web UI without changing business logic
- **Maintainability**: Changes in one layer don't cascade to others

**Example**:
- `manager/control.py` orchestrates workflows but doesn't know about folder structures
- `classification/folder.py` handles folder logic but doesn't know about CLI/API
- `extract/extract.py` reads files but doesn't know about classification logic

### Abstraction Rationale

**1. Folder as First-Class Citizen (`classification/folder.py`)**
- Represents a work folder with its own lifecycle (classify → save → rename → finish)
- Encapsulates all folder-related operations (move, merge, classify)
- State machine pattern: folders progress through states (other → code → classified → finished)

**2. Crawler Separation (`crawler/`)**
- **Single Responsibility**: Only responsible for fetching external data
- **Dependency Inversion**: Folder class depends on crawler interface, not implementation
- Can inject different crawlers (DLsite, other sources) via `use_crawler()`

**3. Extract vs Classification Split**
- **Extract** (`extract/`): "What data exists?" - reads file system, creates models
- **Classification** (`classification/`): "How to organize?" - applies business rules
- Separation allows: batch reading without classification, or reclassification without re-reading

**4. Async Queue Pattern (`spkg/sasync/`)**
- **SAsyncRunner**: Work pool pattern for concurrent async operations
- Why? Disk I/O and network requests are slow; async maximizes throughput
- `read` queue feeds workers, `finish` queue tracks completion

**5. Tag Conversion Table (`extract/structure.py`)**
- Maps Japanese field names to English programmatic names
- **Open/Closed Principle**: Adding new fields requires only table update, not code changes
- **Single Source of Truth**: One place to manage field mappings

## SOLID Principles Implementation

### Single Responsibility Principle (SRP)

Each module has ONE reason to change:

- **`crawler/work.py`**: Changes only if DLsite HTML structure changes
- **`extract/extract.py`**: Changes only if file system structure changes
- **`classification/folder.py`**: Changes only if folder organization rules change
- **`server.py`**: Changes only if API contract changes
- **`tools/move.py`**: Changes only if file operation requirements change

### Open/Closed Principle (OCP)

- **Crawler injection**: `Folder.use_crawler()` allows new crawlers without modifying Folder class
- **Tag conversion table**: New metadata fields added via table, not code modification
- **Async runner**: Can add new work types to queue without changing runner implementation

### Liskov Substitution Principle (LSP)

- **Pydantic models** (`Work`, `Company`, `Tag`): All models are immutable value objects
- **CommonCrawler methods**: `@classmethod` ensures consistent behavior across all callers
- Functions expecting `Folder` can work with any folder, regardless of classification state

### Interface Segregation Principle (ISP)

- **Tools module**: Each file (`move.py`, `check.py`, `scan.py`) provides narrow interfaces
- Clients import only what they need: `from tools import move_folder` (not entire tools module)
- **Manager control**: Each manager function is independent (ISP at function level)

### Dependency Inversion Principle (DIP)

- **Manager depends on abstractions**: Imports from classification/crawler, not concrete implementations
- **FastAPI server**: Depends on `ExtractFolder` interface, not file system implementation
- **Folder uses crawler**: Depends on crawler having `get_use_code()` method, not specific crawler type

## Clean Code Rules & Standards

### Function Size & Responsibility

**CRITICAL RULE**: Each function must:
1. **Do ONE thing** (Single Level of Abstraction)
2. **Maximum 45 lines** (including whitespace/comments)
3. **No nested functions over 2 levels deep**
4. **Named clearly** (verb for functions, noun for classes)

**Current Violations to Fix**:
- `classification/folder.py:classify()` - 84 lines → Split into: `_prepare_info_folder()`, `_save_new_data()`, `_merge_old_data()`, `_finalize_info_folder()`
- `extract/extract.py:scan_work()` - 43 lines (acceptable but should extract error handling)
- `server.py:convert_work_to_response()` - 96 lines → Split into: `_extract_basic_info()`, `_extract_metadata()`, `_extract_images()`
- `server.py:get_works()` - 130 lines → Split into: `_apply_filters()`, `_apply_sorting()`, `_paginate_results()`

### Naming Conventions

**Classes**: PascalCase, noun phrases
- `ExtractFolder`, `DLsiteWorkCrawler`, `CommonCrawler` ✓

**Functions**: snake_case, verb phrases
- `scan_file()`, `get_work_detail()`, `move_folder()` ✓

**Private functions**: Prefix with `_`
- `_scan()`, `_work_count()`, `_load()` ✓

**Async functions**: Same rules, no special prefix needed
- `async def scan_file()`, `async def classify()` ✓

### Error Handling

**Current Pattern** (good):
```python
try:
    # operation
except Exception as e:
    logging.error(f"Context: {e}")
    # handle or re-raise
```

**Improvement Needed**:
- Avoid bare `except:` (seen in `extract.py:121`)
- Always log context with errors
- Use specific exceptions (`FileNotFoundError` not `Exception`)

### Comments & Documentation

**Good examples**:
- `structure.py`: Japanese comments explain metadata fields
- `conversion_table`: Self-documenting mapping

**Needs improvement**:
- Add docstrings to complex functions (e.g., `make_tag()`, `classify()`)
- Document async queue pattern usage
- Add type hints to all function signatures

## Data Storage Format

Works are stored in a structured directory format:
```
[CompanyName]_[CompanyID]/
  └── [WorkID]_[CompanyName]_[CompanyID] WorkTitle/
      └── [WorkID]_info/
          ├── [WorkID]_img_main.jpg
          ├── [WorkID]_img_smp*.jpg
          ├── code.tag
          ├── title.tag
          ├── company.tag
          ├── genre.tag
          ├── my_rating.tag      # User data
          ├── my_collection.tag   # User data
          └── ... (other metadata .tag files)
```

**Why `.tag` files?**
- Simple, human-readable format
- Each field is independently updateable
- No database dependencies
- Easy backup/version control

## Backend Architecture (Python)

### Core Package Structure

**Package Structure:**
- `crawler/`: Web scraping for DLsite metadata (work details, company info)
  - **Responsibility**: External data acquisition ONLY
  - Uses aiohttp for async HTTP requests
  - BeautifulSoup4 for HTML parsing
  - Pattern: `CommonCrawler` provides shared HTTP/image fetching

- `extract/`: File system scanning and metadata extraction
  - **Responsibility**: File system → Domain model transformation
  - `ExtractFolder`: Main orchestrator for scanning operations
  - `structure.py`: Pydantic models (Company, Work, WorkInfo, Tag)
  - Async batch processing via `SAsyncRunner`

- `classification/`: Folder classification and organization logic
  - **Responsibility**: Business rules for folder organization
  - `Folder` class: State machine for work folders
  - `classification.py`: Top-level classification workflows
  - Pattern: Regex-based folder name matching

- `manager/`: High-level workflow orchestration
  - **Responsibility**: Coordinate multi-step workflows
  - Façade pattern over classification, crawler, extract
  - User interaction entry points
  - Each manager handles ONE workflow type

- `tools/`: Pure utility functions
  - **Responsibility**: Reusable file/folder operations
  - NO business logic, NO state
  - Functions: `move_folder()`, `check_and_make_folder()`, `extract_folder_top()`

- `common/`: Shared constants and helpers
  - **Responsibility**: Cross-cutting concerns
  - `regex.py`: Centralized regex patterns (DRY principle)
  - `net.py`: HTTP headers and network config
  - `dlsite.py`: DLsite URL constants

- `compare/`: File/folder comparison utilities
  - **Responsibility**: Duplicate detection and comparison

- `spkg/`: Support packages (internal libraries)
  - `sasync/`: Async execution patterns
    - `SAsync`: Event loop wrapper with cleanup
    - `SAsyncRunner`: Work pool for concurrent async tasks
  - `logs/`: Colored logging decorators

### Frontend (Nuxt.js)

- **Location**: `dlsite_classification_web/`
- **Framework**: Nuxt 3 + Vue 3 with Tailwind CSS
- **Pattern**: Single-page application (SPA)
- **Main Component**: `app.vue` - Monolithic (should be refactored)
- **Features**: Search, filtering by company/genre/collection, ratings, image galleries

## Python Environment Management

**CRITICAL: Always use `uv` for Python package management and execution.**

### Why `uv`?
- **Fast**: 10-100x faster than pip for dependency resolution
- **Reliable**: Deterministic installs with lock files
- **Modern**: Built-in virtual environment management
- **Compatible**: Drop-in replacement for pip/pip-tools

### Installation
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip (one time only)
pip install uv
```

## Common Development Commands

### Backend

**Install Dependencies:**
```bash
# First time setup: Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Or use uv's automatic venv management (recommended)
uv pip sync requirements.txt
```

**Add New Package:**
```bash
# Install and add to requirements
uv pip install <package-name>
uv pip freeze > requirements.txt

# Or install specific version
uv pip install <package-name>==<version>
```

**Start API Server:**
```bash
# Using uv to run (automatically uses .venv)
uv run python server.py

# With custom data path:
uv run python server.py --data-path /path/to/data

# Custom port/host:
uv run python server.py --port 8080 --host 127.0.0.1

# Traditional method (if venv already activated)
python server.py
```

**Start CLI Tool:**
```bash
# Using uv (recommended)
uv run python main.py

# Traditional method
python main.py
```

**Run Tests:**
```bash
# Always use the standardized test script
./run_tests.sh

# For verbose output
./run_tests.sh --verbose

# For HTML coverage report
./run_tests.sh --html
```

**Environment Variables:**
- `DLSITE_DATA_PATH`: Default data directory path (falls back to `./test_game_info`, `/mnt/d/R18/DLsite`, or `./data`)

### Frontend

**Development:**
```bash
cd dlsite_classification_web
yarn install
yarn dev  # Starts on localhost:3000 or 3001
```

**Production Build:**
```bash
yarn build
yarn preview
```

## Key Implementation Details

### Async Architecture Pattern

**Why Async Everywhere?**
- I/O-bound operations (file reads, HTTP requests) dominate
- Async allows concurrent operations without threading overhead
- Pattern: Producer-consumer with async queues

**SAsyncRunner Work Pool** (`spkg/sasync/running.py`):
```python
# Producer: Fills work queue
await read_queue.put(async_function_wrapper)

# Consumer: N workers process queue concurrently
await sasync.run(worker_count)  # Creates N async workers
```

**Flow**:
1. Main function creates `SAsyncRunner` with work queue
2. Populates queue with wrapped async functions
3. Spawns N workers (limited to 30 for rate limiting)
4. Each worker pulls from queue with 3-second timeout
5. Workers process until queue empty

**Usage Example** (`manager/manager_auto_classificatiom.py:20-40`):
- Classification process fills queue with crawl+classify tasks
- Each task is independent (can fail without affecting others)
- Concurrency controlled by worker count (default 10, max 30)

### Data Loading Flow (Extract Layer)

**`ExtractFolder.scan_file()` Workflow**:
1. Lists all folders in data path
2. Filters by `REGEX_COMPANY_FOLDER` pattern (`[CompanyName]_[CompanyID]`)
3. For each company folder:
   - Creates async task: `_scan(company_folder)`
   - Task scans work subfolders via `scan_company()`
   - Each work folder parsed by `scan_work()`
4. Executes via async work pool (30 concurrent max)
5. Returns total scan time

**`scan_work()` Tag Reading**:
- Finds `[WorkID]_info/` directory
- Reads all `.tag` files into dict: `{field_name: file_path}`
- Calls `make_tag()` to batch-process all tags asynchronously
- Creates `WorkInfo` model with `Tag` object and image list

**Tag Conversion** (`make_tag()`):
- Takes dict of `{tag_filename: file_path}`
- Launches async tasks for each tag file read
- Maps Japanese names → English via `conversion_table`
- Applies field-specific parsing:
  - `company`, `title`: `{value: url}` dict
  - `introduction`, `code`: Plain string
  - `star`: `(rating_int, count_string)` tuple
  - `my_rating`, `my_collection`: Plain string (user data)
  - Default: `{value: True}` dict (for multi-value fields)

### API Architecture (Server Layer)

**Request Flow**:
```
HTTP Request → FastAPI Route → ExtractFolder (in-memory cache) → Response
```

**Data Lifecycle**:
- Server creates `ExtractFolder(DATA_PATH)` on startup
- First request triggers `scan_file()` if cache empty
- Cache persists for server lifetime (OrderedDict)
- User data updates write directly to `.tag` files AND update cache

**Key Endpoints**:
- `GET /works`: List with filters (search, company, collection, rating, tags)
  - Applies filters sequentially: text → company → collection → rating → tags
  - Sorting: title (default), sale_date, company, rating, collection
  - Pagination: `limit` (default 24) and `offset`
- `GET /work/{code}`: Detail view with full metadata
  - Returns all fields including voice_actor, illustration, scenario, etc.
- `POST /work/{code}/user-data`: Update rating/collection
  - Writes to `my_rating.tag`, `my_collection.tag`, `my_collections.tag`
  - Updates in-memory cache immediately (no full rescan needed)
- `GET /image?path=<path>`: Serves image files
  - Direct file response via `FileResponse`
  - Path must be absolute (security: validate in production)

**CORS Configuration**:
- Allows `localhost:3000`, `localhost:3001`, `127.0.0.1:3000/3001`
- All methods/headers permitted (development setting)

### Classification Workflow (Business Logic Layer)

**Folder State Machine** (`classification/folder.py`):

```
[Unclassified] → check_folder_package() → [Packaged]
                ↓
        classification_type()
                ↓
   [has code] ──→ move to 'code/' folder
   [no code]  ──→ move to 'other/' folder
                ↓
        use_crawler() + get_info()
                ↓
           classify()
                ↓
        [Classified with metadata]
                ↓
            finish()
                ↓
        [Moved to company folder]
```

**Key Methods**:
- `check_folder_package()`: Recursively unwraps nested single-child folders
- `classification_type()`: Regex match for DLsite code → 'code' or 'other'
- `classify()`: Saves metadata to `[code]_info/` folder
  - Preserves user custom tags (`my_rating.tag`, etc.) during updates
  - Optional `merge_tags=True` merges old and new metadata
  - Atomic operation: writes to temp folder, then replaces
- `finish()`: Moves to final company folder structure

### Web Scraping Pattern (Crawler Layer)

**`DLsiteWorkCrawler.get_use_code()` Flow**:
1. Constructs URL from code prefix (RJ → `dlsite.com/maniax/work/`, BJ → `/books/work/`)
2. Fetches HTML via `CommonCrawler.get_request()`
3. Parses BeautifulSoup object via `format()`
4. Extracts:
   - Title from `<h1>`
   - Company from `.maker_name` span
   - Metadata from `#work_outline` table rows
   - Introduction from `.work_parts_area` div
   - Images from `data-src` attributes (async batch download)
5. Returns dict with Japanese field names (converted later by `make_tag()`)

**Error Handling**:
- Invalid code: Raises `ValueError('Not Code!')`
- Empty response: Raises `ValueError('Not Data!')`
- Network errors: Propagate to caller (caught by manager layer)

### Metadata Normalization (Server Layer)

**Problem**: DLsite data has inconsistencies
- Multiple genres separated by `/` or `,`
- Compound formats like "動画あり音声あり" (has video, has audio)
- Duplicate entries with slight differences (whitespace, trailing chars)

**Solution Functions** (all in `server.py`):

1. **`normalize_and_deduplicate_list(items)`**:
   - Strips whitespace and special chars (`/`)
   - Removes duplicates (case-sensitive, as Japanese)
   - Returns sorted list

2. **`split_and_normalize_formats(format_string)`**:
   - Splits on `/` or `,`
   - Detects compound terms: "動画あり音声あり" → ["動画あり", "音声あり"]
   - Normalizes common patterns (video/audio/music markers)
   - Returns deduplicated list

3. **`smart_merge_similar_items(items)`**:
   - Groups items differing only in whitespace
   - Returns `[{name: str, count: int}]` sorted by frequency

**Applied To**:
- Work formats: `work_format` field
- File formats: `file_format` field
- Genres: In-memory during API response (not persisted)

### Frontend-Backend Integration

**Image Loading**:
- Frontend: `<img :src="/image?path=/absolute/path/to/image.jpg">`
- Backend: Serves via `FileResponse` (no caching headers currently)
- **Security Note**: Path traversal vulnerability if user controls path

**Work Code as Primary Key**:
- Frontend search/filters use work code for detail navigation
- API endpoints use `{code}` path parameter
- Unique across entire DLsite (RJ/BJ/VJ codes are globally unique)

**User Data Persistence**:
- Frontend: POST to `/work/{code}/user-data` with `{rating, collection, collections}`
- Backend: Writes to 3 files atomically, updates cache
- Immediate consistency (no eventual consistency concerns)

## Code Quality Requirements

### Function Refactoring Guidelines

**When to Split a Function**:
1. Exceeds 45 lines (including whitespace/comments)
2. Has multiple levels of abstraction (mixing high-level logic with low-level details)
3. Has more than one reason to change (violates SRP)
4. Cannot be understood without reading implementation (poor abstraction)

**How to Split** (Extract Method Refactoring):

**Example: `server.py:convert_work_to_response()` (96 lines)**

Current structure:
```python
def convert_work_to_response(work, work_folder):
    # 20 lines: basic field extraction
    # 30 lines: genre deduplication
    # 20 lines: work format splitting/normalization
    # 10 lines: age rating, file size
    # 10 lines: image extraction
    # 6 lines: build response object
```

Refactored:
```python
def convert_work_to_response(work, work_folder):
    basic_info = _extract_basic_fields(work)
    metadata = _extract_metadata_fields(work)
    images = _extract_image_urls(work)
    return WorkResponse(**{**basic_info, **metadata, **images})

def _extract_basic_fields(work):
    """Extract title, company, code (10 lines)"""

def _extract_metadata_fields(work):
    """Extract genre, format, age, dates (20 lines)"""

def _extract_image_urls(work):
    """Find main and sample images (10 lines)"""
```

**Benefits**:
- Each function has ONE clear purpose
- Easy to unit test individual extractors
- Can reuse extractors in other contexts
- Self-documenting via function names

### Type Hints Standard

**Required for**:
- All public functions/methods
- Function parameters
- Return types

**Example** (current code often missing):
```python
# Bad (missing hints)
def get_table(self, limit=100, offset=0):
    return list(islice(...))

# Good
def get_table(self, limit: int = 100, offset: int = 0) -> list[tuple[str, Company]]:
    return list(islice(...))
```

**Complex Types** (use `typing` module):
```python
from typing import Optional, List, Dict, Tuple, Union

async def make_tag(self, tags_table: dict[str, str]) -> Tag:
    ...

def get_all_table(self) -> OrderedDict[str, Company]:
    ...
```

### Documentation Standard

**Docstring Format** (Google style):
```python
async def scan_work(self, path: str, code: str) -> WorkInfo:
    """Scan a work folder and extract metadata.

    Reads all .tag files from [code]_info directory and creates
    a WorkInfo object with parsed metadata and image list.

    Args:
        path: Absolute path to work folder
        code: DLsite work code (e.g., 'RJ123456')

    Returns:
        WorkInfo object with tag data and image filenames

    Raises:
        FileNotFoundError: If [code]_info directory doesn't exist
        ValueError: If tag parsing fails
    """
```

**When Required**:
- All public classes (class-level docstring)
- All public methods/functions with complex logic
- Any function over 20 lines
- Functions with non-obvious parameters or return values

**Not Required**:
- Simple utility functions with obvious purpose (`check_and_make_folder`)
- Private methods with clear names (`_work_count`, `_load`)
- One-liner functions

## Development Patterns & Best Practices

### Adding New Metadata Fields

**Full Workflow**:
1. **Update Domain Model** (`extract/structure.py`):
   ```python
   class Tag(BaseModel):
       ...
       new_field: Optional[dict[str, Any]] = None
   ```

2. **Add Conversion Mapping** (`extract/structure.py`):
   ```python
   conversion_table = {
       ...
       "新しいフィールド": "new_field",  # Japanese → English
   }
   ```

3. **Handle Parsing** (`extract/extract.py:make_tag()`):
   - If default dict format works: No change needed
   - If special format: Add to `if eng_name in [...]` conditions

4. **API Response** (`server.py:convert_work_to_response()`):
   ```python
   new_field = []
   if tag.new_field and isinstance(tag.new_field, dict):
       new_field = list(tag.new_field.keys())
   ```

5. **Update Response Model** (`server.py`):
   ```python
   class WorkResponse(BaseModel):
       ...
       new_field: List[str]
   ```

6. **Frontend Display** (`dlsite_classification_web/app.vue`):
   - Add to detail view template
   - Add filter if needed

### Adding API Endpoints

**Pattern**:
```python
@app.get("/new-endpoint")
async def get_new_data(
    param: str = Query(None, description="Filter parameter")
):
    """Endpoint description.

    Args:
        param: Parameter description

    Returns:
        Response structure description
    """
    # Ensure data loaded
    if not extract_data.classification_table:
        await extract_data.scan_file()

    # Process data
    results = []
    for company_name, company_data in extract_data.classification_table.items():
        for work_folder, work in company_data.work_item.items():
            if meets_criteria(work, param):
                results.append(transform(work))

    return {"results": results}
```

**Best Practices**:
- Always check if data is loaded (`classification_table` empty check)
- Use Pydantic models for request/response validation
- Add query parameter descriptions
- Return structured responses (not raw dicts)
- Handle errors with `HTTPException(status_code=..., detail=...)`

### Async Function Guidelines

**When to Use `async`**:
- File I/O (reading `.tag` files, images)
- Network I/O (HTTP requests to DLsite)
- Database operations (if added)
- Any operation that blocks

**When NOT to Use `async`**:
- Pure computation (sorting, filtering in-memory data)
- Simple data transformations
- Regex matching
- Path manipulations

**Await ALL Async Calls**:
```python
# Bad (missing await)
data = raed_data(file_path)  # Returns coroutine object!

# Good
data = await raed_data(file_path)
```

**Batch Async Operations with `asyncio.gather()`**:
```python
# Sequential (slow)
for file in files:
    await read_file(file)

# Concurrent (fast)
await asyncio.gather(*[read_file(f) for f in files])
```

### Error Handling Strategy

**Layered Approach**:

1. **Infrastructure Layer** (`tools/`, `crawler/`):
   - Catch specific exceptions (FileNotFoundError, aiohttp errors)
   - Log with context
   - Re-raise or return None/empty based on recoverability

2. **Business Logic Layer** (`classification/`, `extract/`):
   - Catch infrastructure exceptions
   - Apply fallback logic (e.g., empty tag if file missing)
   - Log warnings for partial failures
   - Raise custom exceptions for complete failures

3. **Manager Layer** (`manager/`):
   - Catch business logic exceptions
   - Log errors with full context
   - Continue with next item (don't let one failure stop batch)
   - Track failure count

4. **Presentation Layer** (`server.py`, `main.py`):
   - Catch all unhandled exceptions
   - Return user-friendly messages (API) or prompts (CLI)
   - Log for debugging

**Example** (from `classification/folder.py:classify()`):
```python
try:
    # Main operation
    await self._save_images(temp_info_folder_path)
    await asyncio.gather(*[...])  # Save tags

    # Success path
    if os.path.isdir(info_folder_path):
        shutil.rmtree(info_folder_path)
    os.rename(temp_info_folder_path, info_folder_path)

except Exception as e:
    # Failure path: cleanup and re-raise
    if os.path.isdir(temp_info_folder_path):
        shutil.rmtree(temp_info_folder_path)
    Red(logging.error, f"Failed to update info for {code}: {e}")
    raise
```

**Key Principle**: Operations should be atomic where possible (temp folder pattern)

## Testing & Data

### Test Data Setup
- **Location**: `./test_game_info/`
- **Structure**: Same as production (company folders with work folders)
- **Purpose**: Development and testing without large dataset
- **Creation**: Manually create or copy subset from production

### Production Data
- **Default Path**: `/mnt/d/R18/DLsite` (WSL mount of Windows D: drive)
- **Override**: Via `--data-path` argument or `DLSITE_DATA_PATH` env var
- **Size**: Potentially thousands of works (scan time: minutes)

### API Testing

**Manual Testing**:
```bash
# Start server
python server.py --data-path ./test_game_info

# Test endpoints (in another terminal)
curl http://localhost:8001/status
curl http://localhost:8001/works?limit=5
curl http://localhost:8001/work/RJ123456
```

**Trigger Manual Rescan**:
```bash
curl http://localhost:8001/scan
```

**Check System Health**:
```bash
curl http://localhost:8001/status
# Returns: {status, total_companies, total_works, data_path}
```

## Common Pitfalls & Solutions

### 1. Async Function Not Awaited
**Symptom**: Function returns `<coroutine object>` instead of result
**Cause**: Forgot `await` keyword
**Solution**: Always `await` async function calls

### 2. Bare Except Catching Too Much
**Symptom**: Hard to debug errors, swallows unexpected exceptions
**Cause**: `except:` or `except BaseException` without re-raise
**Solution**: Use specific exceptions, log before handling

### 3. Mutating Shared State
**Symptom**: Race conditions in async code
**Cause**: Multiple async tasks modifying same dict/list
**Solution**: Use immutable data structures (Pydantic models) or locks

### 4. File Path Encoding Issues
**Symptom**: `UnicodeEncodeError` or `FileNotFoundError` with Asian characters
**Cause**: Default encoding not UTF-8 on Windows
**Solution**: Always open files with `encoding='utf-8'`

### 5. Long Functions Difficult to Test
**Symptom**: Can't test specific logic without full setup
**Cause**: Function does too many things (violates SRP)
**Solution**: Extract smaller functions, each testable independently

## Architecture Evolution Notes

### Current Technical Debt

1. **`server.py` Too Large** (706 lines)
   - Should split into: `routes/`, `models/`, `services/`
   - Mix of concerns: routing, business logic, data transformation

2. **`classification/folder.py` God Object** (329 lines)
   - Handles: folder manipulation, metadata, crawler interaction, file I/O
   - Should split into: `FolderMover`, `FolderClassifier`, `MetadataSaver`

3. **No Automated Tests**
   - Manual testing only
   - Should add: pytest with fixtures for test data

4. **Frontend Monolithic** (`app.vue` 36KB)
   - Single file handles: routing, state, UI, API calls
   - Should split into: pages, components, composables, API layer

5. **No Input Validation** (security)
   - Server accepts any file path in `/image` endpoint (path traversal risk)
   - Should validate: paths are within data directory

### Recommended Next Steps

**High Priority**:
1. Add type hints to all functions (improves IDE support, catches bugs)
2. Split large functions (>45 lines) into smaller ones
3. Add docstrings to public APIs
4. Validate file paths in `/image` endpoint

**Medium Priority**:
1. Split `server.py` into modules
2. Refactor `Folder` class into smaller classes
3. Add basic unit tests for pure functions (tools, common) - **Use `./run_tests.sh`**
4. Frontend: Extract reusable components

**Low Priority**:
1. Add integration tests - **Use `./run_tests.sh`**
2. Performance profiling and optimization
3. Add caching layer (Redis) for large datasets - **Install with `uv pip install redis`**
4. Database migration for better querying (SQLite/PostgreSQL) - **Install with `uv pip install sqlalchemy`**

## Development Workflow with `uv`

### Daily Development

```bash
# Activate virtual environment (if not using uv run)
source .venv/bin/activate

# Update dependencies when requirements.txt changes
uv pip sync requirements.txt

# Run development server
uv run python server.py --data-path ./test_game_info

# Run CLI tool
uv run python main.py

# Run tests
./run_tests.sh
```

### Adding Dependencies

```bash
# Install new package
uv pip install <package-name>

# Install development dependencies
uv pip install pytest pytest-asyncio pytest-cov

# Update requirements.txt
uv pip freeze > requirements.txt

# Or manually add to requirements.txt and sync
echo "new-package==1.2.3" >> requirements.txt
uv pip sync requirements.txt
```

### Testing Workflow

```bash
# Run all tests (standardized)
./run_tests.sh

# Verbose output
./run_tests.sh --verbose

# Generate HTML coverage report
./run_tests.sh --html

# Quick test (no coverage)
./run_tests.sh --quick
```

### Virtual Environment Management

```bash
# Create new virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.13

# Remove virtual environment
rm -rf .venv

# Recreate environment (useful for cleaning)
rm -rf .venv && uv venv && uv pip sync requirements.txt
```

## Package Management Best Practices

### DO:
- ✅ Always use `uv run` for executing Python scripts
- ✅ Use `uv pip install` for adding packages
- ✅ Use `uv pip sync` to ensure exact dependency match
- ✅ Update `requirements.txt` after installing new packages
- ✅ Use `uv venv` to create virtual environments

### DON'T:
- ❌ Don't use `pip` directly (use `uv pip` instead)
- ❌ Don't use `python -m pip` (use `uv pip` instead)
- ❌ Don't forget to update `requirements.txt` after installing packages
- ❌ Don't commit `.venv/` to git (already in `.gitignore`)
- ❌ Don't mix `pip` and `uv pip` in the same environment

### Example Workflow: Adding a New Feature

```bash
# 1. Ensure clean environment
uv pip sync requirements.txt

# 2. Install new dependency if needed
uv pip install new-library

# 3. Update requirements
uv pip freeze > requirements.txt

# 4. Write code
# ... edit files ...

# 5. Run application to test
uv run python server.py --data-path ./test_game_info

# 6. Run tests
./run_tests.sh

# 7. Commit changes (including requirements.txt)
git add requirements.txt dlsite_classification/
git commit -m "feat: add new feature"
```
