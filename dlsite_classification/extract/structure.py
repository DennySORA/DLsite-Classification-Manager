from typing import Any

from pydantic import BaseModel


conversion_table = {
    "code": "code",
    "title": "title",
    "company": "company",
    "star": "star",
    "introduction": "introduction",
    "request_failed": "request_failed",
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
    code: str | None = None
    star: tuple[int, str] | None = None
    title: dict[str, Any] | None = None
    company: dict[str, Any] | None = None
    introduction: str | None = None
    request_failed: str | None = None

    # シリーズ名 - Series name
    series: dict[str, Any] | None = None
    # ジャンル - Genre
    genre: dict[str, Any] | None = None
    # ファイル容量 - File capacity
    file_capacity: dict[str, Any] | None = None
    # ファイル形式 - File format
    file_format: dict[str, Any] | None = None
    # 作品形式 - Work format
    work_format: dict[str, Any] | None = None
    # 声優 - Voice actor
    voice_actor: dict[str, Any] | None = None
    # 年齢指定 - Age designation
    age: dict[str, Any] | None = None
    # 販売日 - Sale date
    sale_date: dict[str, Any] | None = None
    # 更新情報 - Update
    update_date: dict[str, Any] | None = None
    # 動作環境 - Operating environment
    operating_environment: dict[str, Any] | None = None
    # イラスト - Illustration
    illustration: dict[str, Any] | None = None
    # シナリオ - Scenario
    scenario: dict[str, Any] | None = None
    # 作者 - Author
    author: dict[str, Any] | None = None
    # ページ数 - Number of pages
    pages: dict[str, Any] | None = None
    # イベント - Event
    event: dict[str, Any] | None = None
    # 音楽 - Music
    music: dict[str, Any] | None = None
    # その他 - Other
    other: dict[str, Any] | None = None
    # 対応言語 - Supported languages
    languages: dict[str, Any] | None = None

    # User custom fields
    my_rating: str | None = None  # User's personal rating (1-5 stars)
    my_collection: str | None = None  # User's collection category
    my_collections: list[str] | None = None  # User's multiple collection categories


class WorkInfo(BaseModel):
    path: str
    tag: Tag
    images: list[str]


class Work(BaseModel):
    path: str
    code: str
    name: str
    info: WorkInfo | None = None


class Company(BaseModel):
    path: str
    name: str
    work_item: dict[str, Work]
