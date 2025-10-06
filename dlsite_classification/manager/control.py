from dlsite_classification.spkg.logs import Blue, Green, Yellow

from .languages import MenuLanguage
from .manager_auto_classificatiom import classification_depth_one_folder_func
from .manager_company_archive import create_company_archives
from .manager_compare_folder_name import (
    compare_file_hash_func,
    compare_folder_name_func,
)
from .manager_move_folder_to_top import classification_folder_move_top_func
from .manager_validate_structure import validate_structure_func
from .manager_work_update import work_update_func


def _print_menu_item(number, title, description):
    """列印選單項目。

    Args:
        number: 選項編號
        title: 標題
        description: 功能說明
    """
    Blue(print, f"  [{number}] {title}")
    Yellow(print, f"      → {description}\n")


async def user_control():
    while True:
        # 取得當前語言的文字
        title = MenuLanguage.get_text("title")
        exit_text = MenuLanguage.get_text("exit")
        select_prompt = MenuLanguage.get_text("select_prompt")
        language_prompt = MenuLanguage.get_text("language_prompt")

        Blue(print, "\n" + "=" * 80)
        Blue(print, title.center(80))
        Blue(print, "=" * 80 + "\n")

        # 顯示語言切換選項
        Green(print, language_prompt)
        print()

        # 顯示所有選單項目
        for number in range(1, 11):
            item = MenuLanguage.get_text("menu_items", str(number))
            _print_menu_item(str(number), item["title"], item["desc"])

        Blue(print, "=" * 80)
        Green(print, f"\n  -1: {exit_text}\n")
        try:
            select = int(input(f"{select_prompt}: "))
        except ValueError:
            continue

        if select == 0:
            # 切換語言
            MenuLanguage.show_language_selection()
            continue
        if select == -1:
            return
        await user_select(select)


async def user_select(select):
    if select == 1:
        await classification_depth_one_folder_func()
    elif select == 2:
        await classification_folder_move_top_func()
    elif select == 3:
        path = input("Input path:")
        await classification_folder_move_top_func(path)
        await classification_depth_one_folder_func(path)
    elif select == 4:
        await work_update_func()
    elif select == 5:
        await work_update_func(is_rename=1)
    elif select == 6:
        await compare_folder_name_func()
    elif select == 7:
        await compare_file_hash_func()
    elif select == 8:
        await validate_structure_func()
    elif select == 9:
        path = input("Input source path: ")
        move_to = input("Input target path (e.g., /mnt/d/R18/DLsite_TEMP): ")
        await validate_structure_func(path, move_to)
    elif select == 10:
        path = input("Input data path: ")
        company_id = input(
            "Input specific company ID (leave empty for all companies): "
        ).strip()
        force = input("Force re-download existing archives? [Y/n]: ").strip().upper()
        await create_company_archives(
            data_path=path if path else None,
            specific_company_id=company_id if company_id else None,
            force_update=force == "Y",
        )
