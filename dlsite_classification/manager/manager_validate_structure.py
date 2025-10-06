import logging
import os
import shutil

from dlsite_classification.common.regex import REGEX_COMPANY_FOLDER, REGEX_RJ
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red, Yellow


async def validate_structure_func(path=None, move_to=None):
    """驗證已分類資料的資料夾結構和內容。

    檢查每個公司資料夾中的作品資料夾格式是否正確，
    以及是否包含必要的 info 資料夾。
    可選擇將有問題的資料夾移動到另一個目錄。

    Args:
        path: 資料路徑，如果為 None 則要求使用者輸入
        move_to: 移動目標路徑，如果為 None 則只驗證不移動
    """
    if path is None:
        path = input("Input path:")

    if not os.path.isdir(path):
        Red(logging.error, f"Path does not exist: {path}", stack_info=False)
        return

    Blue(logging.info, "========== Start Validating Structure ==========")

    # 儲存問題資料夾
    issues = {
        "invalid_work_format": [],  # 作品資料夾格式錯誤
        "missing_info": [],  # 缺少 info 資料夾的作品
        "missing_code": [],  # 資料夾名稱中沒有代碼的作品
        "invalid_company_format": [],  # 公司資料夾格式錯誤
        "code_only_folder": [],  # 只有代碼的資料夾（缺少標題）
    }

    total_companies = 0
    total_works_scanned = 0
    total_folders_checked = 0

    # 直接掃描檔案系統，不依賴 ExtractFolder 的過濾
    try:
        company_folders = [
            d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))
        ]
    except Exception as e:
        Red(logging.error, f"Failed to list directory: {e}")
        return

    Cyan(logging.info, f"Found {len(company_folders)} top-level folders")

    for company_folder_name in company_folders:
        company_folder_path = os.path.join(path, company_folder_name)

        # 檢查這是否真的是公司資料夾（不是作品資料夾）
        # 公司資料夾不應該包含作品代碼，作品資料夾才有代碼
        is_company_folder = REGEX_COMPANY_FOLDER.match(company_folder_name)
        has_work_code = REGEX_RJ.search(company_folder_name)

        # 如果既符合公司格式，又沒有作品代碼，才是真正的公司資料夾
        if is_company_folder and not has_work_code:
            total_companies += 1
        elif not is_company_folder and not has_work_code:
            # 不符合公司格式，也沒有作品代碼 - 這是有問題的資料夾
            total_companies += 1
            issues["invalid_company_format"].append(
                {
                    "path": company_folder_path,
                    "name": company_folder_name,
                    "reason": "格式不符合 [CompanyName]_[CompanyID]",
                }
            )
        else:
            # 包含作品代碼的，可能是誤放在頂層的作品資料夾
            # 也算一個公司資料夾（即使格式不對）
            total_companies += 1

        # 檢查公司資料夾內的所有子資料夾
        try:
            work_folders = [
                d
                for d in os.listdir(company_folder_path)
                if os.path.isdir(os.path.join(company_folder_path, d))
            ]
        except Exception as e:
            Red(logging.error, f"Failed to list {company_folder_path}: {e}")
            continue

        for work_folder_name in work_folders:
            total_folders_checked += 1
            work_folder_path = os.path.join(company_folder_path, work_folder_name)

            # 檢查作品資料夾是否包含代碼
            code_match = REGEX_RJ.search(work_folder_name)

            if not code_match:
                # 沒有找到作品代碼
                issues["missing_code"].append(
                    {
                        "company": company_folder_name,
                        "path": work_folder_path,
                        "name": work_folder_name,
                    }
                )
                continue

            code = code_match.group()
            total_works_scanned += 1

            # 檢查作品資料夾格式：應該是 [CODE]_[CompanyName]_[CompanyID] Title
            # 最簡格式應該至少包含 CODE_
            if not _is_valid_work_folder_format(work_folder_name, code):
                issues["code_only_folder"].append(
                    {
                        "company": company_folder_name,
                        "code": code,
                        "path": work_folder_path,
                        "name": work_folder_name,
                        "reason": "只有代碼，缺少公司資訊和標題",
                    }
                )
                # 繼續檢查 info 資料夾

            # 檢查是否有 info 資料夾
            expected_info_folder = f"{code}_info"
            info_folder_path = os.path.join(work_folder_path, expected_info_folder)

            if not os.path.isdir(info_folder_path):
                issues["missing_info"].append(
                    {
                        "company": company_folder_name,
                        "code": code,
                        "path": work_folder_path,
                        "name": work_folder_name,
                        "expected_info": expected_info_folder,
                    }
                )

    # 輸出統計資訊
    Blue(logging.info, "========== Validation Summary ==========")
    Cyan(logging.info, f"Total Company Folders: {total_companies}")
    Cyan(logging.info, f"Total Subfolders Checked: {total_folders_checked}")
    Cyan(logging.info, f"Total Works with Code: {total_works_scanned}")

    # 輸出問題統計
    total_issues = sum(len(v) for v in issues.values())
    if total_issues == 0:
        Green(logging.info, "✓ All folders are valid!")
    else:
        Yellow(logging.warning, f"Found {total_issues} issues")

    # 列印詳細問題表格
    _print_issues_table(issues)

    # 如果指定了移動目標，詢問是否移動問題資料夾
    if move_to is not None and total_issues > 0:
        await _move_problematic_folders(issues, path, move_to)

    Blue(logging.info, "========== Validation Complete ==========")


async def _move_problematic_folders(issues, source_root, target_root):
    """移動有問題的資料夾到目標目錄，保留相對路徑結構。

    Args:
        issues: 問題資料夾字典
        source_root: 源根目錄
        target_root: 目標根目錄
    """
    Blue(logging.info, "\n========== Move Problematic Folders ==========")

    # 收集所有需要移動的資料夾路徑（使用 set 去重）
    folders_to_move = {}  # path -> item

    # 從各類問題中收集路徑
    for issue_type, issue_list in issues.items():
        for item in issue_list:
            if "path" in item:
                path = item["path"]
                # 只保留第一次出現的問題類型
                if path not in folders_to_move:
                    folders_to_move[path] = {
                        "path": path,
                        "name": item.get("name", ""),
                        "type": issue_type,
                    }

    folders_list = list(folders_to_move.values())

    if not folders_list:
        Yellow(logging.warning, "No folders to move.")
        return

    Cyan(logging.info, f"Found {len(folders_list)} problematic folders to move")
    Cyan(logging.info, f"Source root: {source_root}")
    Cyan(logging.info, f"Target root: {target_root}")

    # 詢問確認
    Yellow(
        logging.warning,
        "\nThis will move all problematic folders to the target directory.",
    )
    Yellow(logging.warning, "The directory structure will be preserved.")

    confirm = input("\nDo you want to proceed? (yes/no): ").strip().lower()

    if confirm not in ["yes", "y"]:
        Yellow(logging.warning, "Move operation cancelled.")
        return

    # 創建目標根目錄（如果不存在）
    if not os.path.exists(target_root):
        os.makedirs(target_root)
        Green(logging.info, f"Created target root directory: {target_root}")

    # 移動資料夾
    moved_count = 0
    failed_count = 0

    for item in folders_list:
        source_path = item["path"]

        # 計算相對於源根目錄的路徑
        try:
            relative_path = os.path.relpath(source_path, source_root)
            target_path = os.path.join(target_root, relative_path)

            # 創建目標父目錄
            target_parent = os.path.dirname(target_path)
            if not os.path.exists(target_parent):
                os.makedirs(target_parent)

            # 檢查目標是否已存在
            if os.path.exists(target_path):
                Yellow(
                    logging.warning, f"Target already exists, skipping: {target_path}"
                )
                failed_count += 1
                continue

            # 移動資料夾
            shutil.move(source_path, target_path)
            Green(logging.info, f"Moved: {item['name']}")
            Cyan(logging.info, f"  From: {source_path}")
            Cyan(logging.info, f"  To:   {target_path}")
            moved_count += 1

        except Exception as e:
            Red(logging.error, f"Failed to move {source_path}: {e}", stack_info=False)
            failed_count += 1

    # 移動完成統計
    Blue(logging.info, "\n========== Move Summary ==========")
    Green(logging.info, f"Successfully moved: {moved_count} folders")
    if failed_count > 0:
        Red(logging.error, f"Failed to move: {failed_count} folders", stack_info=False)


def _is_valid_work_folder_format(folder_name, code):
    """檢查作品資料夾格式是否正確。

    正確格式應該是：[CODE]_[CompanyName]_[CompanyID] Title
    或至少包含：CODE_

    Args:
        folder_name: 資料夾名稱
        code: 作品代碼

    Returns:
        True 如果格式正確，否則 False
    """
    # 只有代碼（如 "RJ123456"）視為不合格
    if folder_name == code:
        return False

    # 只有方括號包裹的代碼（如 "[RJ123456]"）視為不合格
    if folder_name == f"[{code}]":
        return False

    # 檢查是否有下劃線和公司資訊
    # 標準格式：[CODE]_[Company]_[CompanyID] Title
    # 最簡格式：CODE_至少有其他內容
    if f"{code}_" not in folder_name and f"[{code}]_" not in folder_name:
        return False

    return True


def _print_issues_table(issues):
    """以表格形式列印所有問題。

    Args:
        issues: 包含各類問題的字典
    """
    # 1. 公司資料夾格式錯誤
    if issues["invalid_company_format"]:
        Red(logging.error, f"\n{'=' * 80}", stack_info=False)
        Red(
            logging.error,
            f"[1] 公司資料夾格式錯誤 ({len(issues['invalid_company_format'])} 個)",
            stack_info=False,
        )
        Red(logging.error, f"{'=' * 80}", stack_info=False)
        Red(logging.error, f"{'資料夾名稱':<50} | {'問題':<25}", stack_info=False)
        Red(logging.error, f"{'-' * 80}", stack_info=False)

        for item in issues["invalid_company_format"]:
            name = _truncate_string(item["name"], 48)
            reason = _truncate_string(item["reason"], 23)
            Red(logging.error, f"{name:<50} | {reason:<25}", stack_info=False)
            Red(logging.error, f"路徑: {item['path']}", stack_info=False)
            Red(logging.error, f"{'-' * 80}", stack_info=False)

    # 2. 缺少作品代碼的資料夾
    if issues["missing_code"]:
        Red(logging.error, f"\n{'=' * 80}", stack_info=False)
        Red(
            logging.error,
            f"[2] 資料夾名稱中缺少作品代碼 ({len(issues['missing_code'])} 個)",
            stack_info=False,
        )
        Red(logging.error, f"{'=' * 80}", stack_info=False)
        Red(
            logging.error,
            f"{'公司資料夾':<35} | {'作品資料夾名稱':<40}",
            stack_info=False,
        )
        Red(logging.error, f"{'-' * 80}", stack_info=False)

        for item in issues["missing_code"]:
            company = _truncate_string(item["company"], 33)
            name = _truncate_string(item["name"], 38)
            Red(logging.error, f"{company:<35} | {name:<40}", stack_info=False)
            Red(logging.error, f"路徑: {item['path']}", stack_info=False)
            Red(logging.error, f"{'-' * 80}", stack_info=False)

    # 3. 只有代碼的資料夾（格式不完整）
    if issues["code_only_folder"]:
        Yellow(logging.warning, f"\n{'=' * 80}")
        Yellow(
            logging.warning,
            f"[3] 作品資料夾格式不完整 ({len(issues['code_only_folder'])} 個)",
        )
        Yellow(logging.warning, f"{'=' * 80}")
        Yellow(logging.warning, f"{'代碼':<12} | {'公司':<30} | {'資料夾名稱':<30}")
        Yellow(logging.warning, f"{'-' * 80}")

        for item in issues["code_only_folder"]:
            code = item["code"]
            company = _truncate_string(item["company"], 28)
            name = _truncate_string(item["name"], 28)
            Yellow(logging.warning, f"{code:<12} | {company:<30} | {name:<30}")
            Yellow(logging.warning, f"路徑: {item['path']}")
            Yellow(logging.warning, f"原因: {item['reason']}")
            Yellow(logging.warning, f"{'-' * 80}")

    # 4. 缺少 info 資料夾
    if issues["missing_info"]:
        Yellow(logging.warning, f"\n{'=' * 80}")
        Yellow(
            logging.warning, f"[4] 缺少 info 資料夾 ({len(issues['missing_info'])} 個)"
        )
        Yellow(logging.warning, f"{'=' * 80}")
        Yellow(logging.warning, f"{'代碼':<12} | {'公司':<25} | {'作品資料夾':<35}")
        Yellow(logging.warning, f"{'-' * 80}")

        for item in issues["missing_info"]:
            code = item["code"]
            company = _truncate_string(item["company"], 23)
            name = _truncate_string(item["name"], 33)
            Yellow(logging.warning, f"{code:<12} | {company:<25} | {name:<35}")
            Yellow(logging.warning, f"路徑: {item['path']}")
            Yellow(logging.warning, f"預期 info 資料夾: {item['expected_info']}")
            Yellow(logging.warning, f"{'-' * 80}")


def _truncate_string(s, max_len):
    """截斷字串並添加省略號。

    Args:
        s: 要截斷的字串
        max_len: 最大長度

    Returns:
        截斷後的字串
    """
    if len(s) <= max_len:
        return s
    return s[: max_len - 2] + ".."
