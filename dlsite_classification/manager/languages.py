"""Multi-language support for menu system."""


class MenuLanguage:
    """Menu language configuration."""

    # 當前語言
    current_language = "zh"  # 預設中文

    # 語言配置
    LANGUAGES = {
        "zh": {
            "name": "中文",
            "title": "DLsite 分類管理器 - 主選單",
            "exit": "退出程式",
            "select_prompt": "請選擇功能",
            "language_prompt": "  0: 切換語言 (Change Language / 言語を変更)",
            "menu_items": {
                "1": {
                    "title": "分類資料夾並自動獲取標籤",
                    "desc": "掃描未分類的資料夾，自動識別 DLsite 作品代碼並下載元數據",
                },
                "2": {
                    "title": "提取資料夾移至頂層",
                    "desc": "將巢狀資料夾中的內容提取到頂層（解壓縮後的整理）",
                },
                "3": {
                    "title": "自動完整分類流程",
                    "desc": "執行完整分類流程：先提取資料夾，再自動分類和下載標籤",
                },
                "4": {
                    "title": "更新作品資訊",
                    "desc": "重新從 DLsite 下載已分類作品的最新元數據（保留自訂標籤）",
                },
                "5": {
                    "title": "更新資料夾名稱",
                    "desc": "根據最新元數據重新命名作品或公司資料夾",
                },
                "6": {
                    "title": "比較資料夾名稱",
                    "desc": "尋找可能重複的作品（根據資料夾名稱相似度）",
                },
                "7": {
                    "title": "比較檔案雜湊值",
                    "desc": "尋找完全相同的檔案（根據檔案內容 hash 比對）",
                },
                "8": {
                    "title": "驗證資料夾結構",
                    "desc": "檢查已分類資料的資料夾格式和 info 資料夾完整性",
                },
                "9": {
                    "title": "驗證並移動問題資料夾",
                    "desc": "檢查資料夾結構，並將有問題的資料夾移動到指定目錄",
                },
                "10": {
                    "title": "建立公司作品檔案庫",
                    "desc": "掃描公司資料夾，建立 ARCHIVE 子資料夾，收錄該公司所有作品的完整資訊",
                },
            },
        },
        "en": {
            "name": "English",
            "title": "DLsite Classification Manager - Main Menu",
            "exit": "Exit",
            "select_prompt": "Select function",
            "language_prompt": "  0: Change Language (切換語言 / 言語を変更)",
            "menu_items": {
                "1": {
                    "title": "Classification folder and auto get tag",
                    "desc": "Scan unclassified folders, auto-identify DLsite work codes and download metadata",
                },
                "2": {
                    "title": "Extract folder move to top",
                    "desc": "Extract nested folder contents to top level (organize after extraction)",
                },
                "3": {
                    "title": "Auto classification (Full workflow)",
                    "desc": "Execute full classification workflow: extract folders first, then auto-classify and download tags",
                },
                "4": {
                    "title": "Update work info",
                    "desc": "Re-download latest metadata from DLsite for classified works (preserve custom tags)",
                },
                "5": {
                    "title": "Update work or company folder name",
                    "desc": "Rename work or company folders based on latest metadata",
                },
                "6": {
                    "title": "Compare folder name",
                    "desc": "Find potentially duplicate works (based on folder name similarity)",
                },
                "7": {
                    "title": "Compare file hash",
                    "desc": "Find identical files (based on file content hash comparison)",
                },
                "8": {
                    "title": "Validate folder structure and info",
                    "desc": "Check folder format and info directory integrity for classified data",
                },
                "9": {
                    "title": "Validate and move problematic folders",
                    "desc": "Check folder structure and move problematic folders to specified directory",
                },
                "10": {
                    "title": "Create Company Works Archive",
                    "desc": "Scan company folders, create ARCHIVE subfolder with complete info for all company works",
                },
            },
        },
        "ja": {
            "name": "日本語",
            "title": "DLsite 分類マネージャー - メインメニュー",
            "exit": "終了",
            "select_prompt": "機能を選択",
            "language_prompt": "  0: 言語を変更 (切換語言 / Change Language)",
            "menu_items": {
                "1": {
                    "title": "フォルダを分類して自動的にタグを取得",
                    "desc": "未分類のフォルダをスキャンし、DLsite作品コードを自動識別してメタデータをダウンロード",
                },
                "2": {
                    "title": "フォルダをトップレベルに抽出",
                    "desc": "ネストされたフォルダの内容をトップレベルに抽出（解凍後の整理）",
                },
                "3": {
                    "title": "自動完全分類フロー",
                    "desc": "完全な分類フローを実行：最初にフォルダを抽出し、その後自動分類してタグをダウンロード",
                },
                "4": {
                    "title": "作品情報を更新",
                    "desc": "分類済み作品の最新メタデータをDLsiteから再ダウンロード（カスタムタグを保持）",
                },
                "5": {
                    "title": "作品またはサークルフォルダ名を更新",
                    "desc": "最新のメタデータに基づいて作品またはサークルフォルダの名前を変更",
                },
                "6": {
                    "title": "フォルダ名を比較",
                    "desc": "重複する可能性のある作品を検索（フォルダ名の類似度に基づく）",
                },
                "7": {
                    "title": "ファイルハッシュを比較",
                    "desc": "完全に同一のファイルを検索（ファイル内容のハッシュ比較に基づく）",
                },
                "8": {
                    "title": "フォルダ構造を検証",
                    "desc": "分類済みデータのフォルダ形式とinfoディレクトリの整合性をチェック",
                },
                "9": {
                    "title": "問題のあるフォルダを検証して移動",
                    "desc": "フォルダ構造をチェックし、問題のあるフォルダを指定したディレクトリに移動",
                },
                "10": {
                    "title": "サークル作品アーカイブを作成",
                    "desc": "サークルフォルダをスキャンし、ARCHIVEサブフォルダを作成してすべての作品情報を保存",
                },
            },
        },
    }

    @classmethod
    def get_text(cls, key, item_number=None):
        """取得當前語言的文字。

        Args:
            key: 文字鍵值
            item_number: 選單項目編號（可選）

        Returns:
            對應的文字
        """
        lang_config = cls.LANGUAGES.get(cls.current_language, cls.LANGUAGES["zh"])

        if item_number is not None:
            return lang_config["menu_items"][item_number]

        return lang_config.get(key, "")

    @classmethod
    def set_language(cls, lang_code):
        """設定語言。

        Args:
            lang_code: 語言代碼 (zh/en/ja)
        """
        if lang_code in cls.LANGUAGES:
            cls.current_language = lang_code
            return True
        return False

    @classmethod
    def get_available_languages(cls):
        """取得可用語言列表。

        Returns:
            語言代碼和名稱的列表
        """
        return [(code, config["name"]) for code, config in cls.LANGUAGES.items()]

    @classmethod
    def show_language_selection(cls):
        """顯示語言選擇選單並返回選擇的語言。

        Returns:
            選擇的語言代碼
        """
        from dlsite_classification.spkg.logs import Blue, Cyan, Green

        Blue(print, "\n" + "=" * 80)
        Blue(print, "Select Language / 選擇語言 / 言語を選択".center(80))
        Blue(print, "=" * 80 + "\n")

        languages = cls.get_available_languages()
        for idx, (code, name) in enumerate(languages, 1):
            marker = "★ " if code == cls.current_language else "  "
            Green(print, f"  {marker}{idx}. {name} ({code})")

        Blue(print, "\n" + "=" * 80)

        while True:
            try:
                choice = int(input("\nSelect (1-3): "))
                if 1 <= choice <= len(languages):
                    selected_code = languages[choice - 1][0]
                    cls.set_language(selected_code)
                    Cyan(
                        print,
                        f"✓ Language changed to: {cls.LANGUAGES[selected_code]['name']}",
                    )
                    return selected_code
            except (ValueError, KeyboardInterrupt):
                continue
