import logging
import os
from pathlib import Path
import shutil
import sys
import time

import pytest


def get_case_target():
    if len(sys.argv) > 1:
        return sys.argv[1].strip()
    return ""


def rotate_log_file():
    src = Path("logs/frame.log")
    if not src.exists():
        return

    dst = src.with_name(f"frame_{int(time.time())}.log")

    # Release FileHandler locks before moving logs on Windows.
    logging.shutdown()

    last_error = None
    for _ in range(10):
        try:
            shutil.move(str(src), str(dst))
            return
        except PermissionError as exc:
            last_error = exc
            time.sleep(0.2)

    raise last_error


if __name__ == '__main__':
    case_target = get_case_target()
    if case_target:
        os.environ["CASE_TARGET"] = case_target
    else:
        os.environ.pop("CASE_TARGET", None)
    pytest.main(["-s", "./test_api/case.py"])
    # 生成并打开allure报告
    time.sleep(3)
    os.system("allure generate ./temps -o ./reports --clean")
    # os.system("allure open ./reports")

    # 复制日志文件
    rotate_log_file()
