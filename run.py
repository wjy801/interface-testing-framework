import os
import shutil
import time
import sys

import pytest


def get_case_target():
    if len(sys.argv) > 1:
        return sys.argv[1].strip()
    return ""


if __name__ == '__main__':
    case_target = get_case_target()
    if case_target:
        os.environ["CASE_TARGET"] = case_target
    else:
        os.environ.pop("CASE_TARGET", None)
    pytest.main(["-s", "./test_api/case.py"])
    # 生成并打开allure报告
    # time.sleep(3)
    # os.system("allure generate ./temps -o ./reports --clean")
    # # os.system("allure open ./reports")
    #
    # # 复制日志文件
    # shutil.move("logs/frame.log","logs/frame_"+str(int(time.time()))+".log")
