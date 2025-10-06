from typing import Any


class CompanyFolder:
    """Placeholder for company-level classification hooks."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.crawler: Any | None = None

    def _check_and_get_origin_info(self) -> None:
        """Validate and prepare origin info for the current company."""
        # Implementation pending: depends on crawler schema.
        return None

    def check_company_info(self) -> None:
        """Check company info consistency."""
        return None

    # ---------------------------------------
    # ---------------------------------------
    # ---------------------------------------

    def use_crawler(self, crawler: Any) -> None:
        self.crawler = crawler
