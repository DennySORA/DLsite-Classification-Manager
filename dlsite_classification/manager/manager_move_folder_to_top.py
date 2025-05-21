from dlsite_classification.classification import classification_folder_move_top


async def classification_folder_move_top_func(path=None):
    if path is None:
        path = input("Input path:")
    classification_folder_move_top(path)
