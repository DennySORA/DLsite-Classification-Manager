
from .manager_auto_classificatiom import classification_depth_one_folder_func
from .manager_move_folder_to_top import classification_folder_move_top_func
from .manager_work_update import work_update_func
from .manager_compare_folder_name import compare_folder_name_func, compare_file_hash_func

from dlsite_classification.spkg.logs import Blue, Green


async def user_control():
    while True:
        Blue(print, """
        Please Select functiom:
        1: classification folder and auto get tag.
        2: Extract folder move to top.
        3: Auto classification.
        4: Update work info.
        5: Update work or company folder name.
        6: Compare folder name.
        7: Compare file hash.
        """)
        Green(print, "\t-1: Exit.\n\n")
        try:
            select = int(input("Select function:"))
        except:
            continue

        if select == -1:
            return
        else:
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
