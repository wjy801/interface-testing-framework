import pytest

from commons.yaml_util import clear_yaml

@pytest.fixture(scope="session",autouse=True)
def clean_extract():
    clear_yaml()
    print("yaml文件清理完毕")
    yield
    print("执行完毕")
