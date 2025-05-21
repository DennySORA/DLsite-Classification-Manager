import logging

from dlsite_classification.classification.folder import Folder
from dlsite_classification.crawler.work import DLsiteWorkCrawler
from dlsite_classification.extract.plug import extract_folder_path
from dlsite_classification.extract.extract import ExtractFolder
from dlsite_classification.spkg.sasync import SAsyncRunner
from dlsite_classification.spkg.logs import Blue, Cyan, Green, Red


async def work_update_func(path=None,is_rename=0):
    if path is None:
        path = input("Input path:")
    if is_rename == 1:
        is_rename = 2 if input("Is change company folder name? [Y/n](default is n, is change work name.):") == 'Y' else 1

    # Classification path folder
    extract_folder = ExtractFolder(path)
    use_time = await extract_folder.scan_file()
    Green(logging.info, f"Extracting Use Time: {use_time}")

    work = []
    for i in extract_folder_path(extract_folder.get_all_table()):
        temp = Folder(i)
        if temp.classification_type(False) != "code":
            continue
        work.append(temp)

    need_run_func_count = len(work)
    if need_run_func_count == 0:
        return

    # Create async runner
    sasync = SAsyncRunner()
    read_queue = sasync.get_read_queue()

    Cyan(logging.info, "==========Start Create Can Crawler Folder ==========")
    # create crawler and injection to file class
    for i in work:
        code = i.file_info.get('code', '')
        if code == '':
            continue
        i.use_crawler(DLsiteWorkCrawler(code=code))
        await read_queue.put(file_doing_manager_wrap(i,is_rename))
        Green(logging.info, f"Create {code} DLsite Crawler.")
    Blue(logging.info, "==========End Create Can Crawler Folder==========")

    # await run
    if need_run_func_count > 10:
        need_run_func_count = 10
    await sasync.run(need_run_func_count)


def file_doing_manager_wrap(folder:Folder,is_rename:int):
    folder_class = folder

    async def doing():
        try:
            if folder_class.crawler is None:
                raise Exception("Not use crawler.")
            try:
                await folder_class.crawler.get_use_code()
            except ValueError:
                await folder_class.set_request_failed()
                return
            folder_class.get_info()
            if is_rename != 0:
                await folder_class.rename(is_rename == 2)
            else:
                await folder_class.classify(False)
        except BaseException as e:
            Red(logging.error, e)
    return doing
