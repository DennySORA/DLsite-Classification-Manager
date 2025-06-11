
from pydantic import BaseModel
from typing import Any, Optional, List

conversion_table = {
    "code": "code",
    "title": "title",
    "company": "company",
    "star": "star",
    "introduction": "introduction",
    "request_failed":"request_failed",
    "シリーズ名": "series",
    "ジャンル": "genre",
    "ファイル容量": "file_capacity",
    "ファイル形式": "file_format",
    "作品形式": "work_format",
    "声優": "voice_actor",
    "年齢指定": "age",
    "販売日": "sale_date",
    "更新情報": "update_date",
    "動作環境": "operating_environment",
    "イラスト": "illustration",
    "シナリオ": "scenario",
    "作者": "author",
    "ページ数": "pages",
    "イベント": "event",
    "音楽": "music",
    "その他": "other",
    "対応言語": "languages",
    # User custom fields
    "my_rating": "my_rating",
    "my_collection": "my_collection",
    "my_collections": "my_collections",
}


class Tag(BaseModel):
    code: Optional[str] = None
    star: Optional[tuple[int, str]] = None
    title: Optional[dict[str, Any]] = None
    company: Optional[dict[str, Any]] = None
    introduction: Optional[str] = None
    request_failed: Optional[str] = None

    # シリーズ名 - Series name
    series: Optional[dict[str, Any]] = None
    # ジャンル - Genre
    genre: Optional[dict[str, Any]] = None
    # ファイル容量 - File capacity
    file_capacity: Optional[dict[str, Any]] = None
    # ファイル形式 - File format
    file_format: Optional[dict[str, Any]] = None
    # 作品形式 - Work format
    work_format: Optional[dict[str, Any]] = None
    # 声優 - Voice actor
    voice_actor: Optional[dict[str, Any]] = None
    # 年齢指定 - Age designation
    age: Optional[dict[str, Any]] = None
    # 販売日 - Sale date
    sale_date: Optional[dict[str, Any]] = None
    # 更新情報 - Update
    update_date: Optional[dict[str, Any]] = None
    # 動作環境 - Operating environment
    operating_environment: Optional[dict[str, Any]] = None
    # イラスト - Illustration
    illustration: Optional[dict[str, Any]] = None
    # シナリオ - Scenario
    scenario: Optional[dict[str, Any]] = None
    # 作者 - Author
    author: Optional[dict[str, Any]] = None
    # ページ数 - Number of pages
    pages: Optional[dict[str, Any]] = None
    # イベント - Event
    event: Optional[dict[str, Any]] = None
    # 音楽 - Music
    music: Optional[dict[str, Any]] = None
    # その他 - Other
    other: Optional[dict[str, Any]] = None
    # 対応言語 - Supported languages
    languages: Optional[dict[str, Any]] = None
    
    # User custom fields
    my_rating: Optional[str] = None  # User's personal rating (1-5 stars)
    my_collection: Optional[str] = None  # User's collection category
    my_collections: Optional[List[str]] = None  # User's multiple collection categories


class WorkInfo(BaseModel):
    path: str
    tag: Tag
    images: list[str]


class Work(BaseModel):
    path: str
    code: str
    name: str
    info: Optional[WorkInfo] = None


class Company(BaseModel):
    path: str
    name: str
    work_item: dict[str, Work]
