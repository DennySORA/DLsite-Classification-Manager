
from pydantic import BaseModel
from typing import Any, Optional

conversion_table = {
    "code": "code",
    "title": "title",
    "company": "company",
    "star": "star",
    "introduction": "introduction",
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
}


class Tag(BaseModel):
    code: Optional[str]
    star: Optional[tuple[int, str]]
    title: Optional[dict[str, Any]]
    company: Optional[dict[str, Any]]
    introduction: Optional[str]

    # シリーズ名 - Series name
    series: Optional[dict[str, Any]]
    # ジャンル - Genre
    genre: Optional[dict[str, Any]]
    # ファイル容量 - File capacity
    file_capacity: Optional[dict[str, Any]]
    # ファイル形式 - File format
    file_format: Optional[dict[str, Any]]
    # 作品形式 - Work format
    work_format: Optional[dict[str, Any]]
    # 声優 - Voice actor
    voice_actor: Optional[dict[str, Any]]
    # 年齢指定 - Age designation
    age: Optional[dict[str, Any]]
    # 販売日 - Sale date
    sale_date: Optional[dict[str, Any]]
    # 更新情報 - Update
    update_date: Optional[dict[str, Any]]
    # 動作環境 - Operating environment
    operating_environment: Optional[dict[str, Any]]
    # イラスト - Illustration
    illustration: Optional[dict[str, Any]]
    # シナリオ - Scenario
    scenario: Optional[dict[str, Any]]
    # 作者 - Author
    author: Optional[dict[str, Any]]
    # ページ数 - Number of pages
    pages: Optional[dict[str, Any]]
    # イベント - Event
    event: Optional[dict[str, Any]]
    # 音楽 - Music
    music: Optional[dict[str, Any]]
    # その他 - Other
    other: Optional[dict[str, Any]]
    # 対応言語 - Supported languages
    languages: Optional[dict[str, Any]]


class WorkInfo(BaseModel):
    path: str
    tag: Tag
    images: list[str]


class Work(BaseModel):
    path: str
    code: str
    name: str
    info: WorkInfo


class Company(BaseModel):
    path: str
    name: str
    work_item: dict[str, Work]
