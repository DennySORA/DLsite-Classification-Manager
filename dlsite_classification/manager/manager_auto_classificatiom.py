import logging

from dlsite_classification.classification import classification_folder, classification_mode
from dlsite_classification.crawler.work import DLsiteWorkCrawler
from dlsite_classification.spkg.sasync import SAsyncRunner
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red


async def classification_depth_one_folder_func(path=None):
    if path is None:
        path = input("Input path:")
    # Classification path folder
    folders = classification_folder(path)
    mode = classification_mode(folders)

    # Get has code folder
    has_code_func = mode.get('code', [])
    need_run_func_count = len(has_code_func)
    if need_run_func_count == 0:
        return

    # Create async runner
    sasync = SAsyncRunner()
    read_queue = sasync.get_read_queue()

    Cyan(logging.info, "==========Start Create Can Crawler Folder ==========")
    # create crawler and injection to file class
    for i in has_code_func:
        code = i.file_info.get('code', '')
        if code == '':
            continue
        i.use_crawler(DLsiteWorkCrawler(code=code))
        await read_queue.put(file_doing_manager_wrap(i))
        Green(logging.info, f"Create {code} DLsite Crawler.")
    Blue(logging.info, "==========End Create Can Crawler Folder==========")

    # await run
    if need_run_func_count > 10:
        need_run_func_count = 10
    await sasync.run(need_run_func_count)


def file_doing_manager_wrap(folder):
    folder_class = folder

    async def doing():
        try:
            await folder_class.crawler.get_use_code()
            folder_class.get_info()
            await folder_class.classify()
            folder_class.finish()
        except BaseException as e:
            Red(logging.error, e)
    return doing
