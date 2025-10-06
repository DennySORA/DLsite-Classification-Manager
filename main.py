from dlsite_classification.manager import user_control
from dlsite_classification.spkg.logs import InitializeLog
from dlsite_classification.spkg.sasync import SAsync


async def main():
    await user_control()


if __name__ == "__main__":
    InitializeLog("./log/")
    SAsync(main).run()
