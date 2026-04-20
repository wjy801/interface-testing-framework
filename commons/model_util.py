from dataclasses import dataclass

import yaml

from commons.requests_util import logger
from commons.yaml_util import read_testcase, read_yaml


# 数据校验类
@dataclass
class CaseInfo:
    # 必填
    feature: str
    story: str
    title: str
    request: dict
    validate: dict
    # 选填
    extract: dict = None
    parametrize: list = None

# 校验测试用例
def verify_yaml(caseinfo: dict,yaml_path):
    try:
        new_caseinfo = CaseInfo(**caseinfo)
        return new_caseinfo
    except Exception:
        logger.error(yaml_path.name+"用例格式错误")
        raise Exception("用例格式错误")

if __name__ == '__main__':
    # a = {'feature': '核心模块', 'story': '获取用户信息','title': '获取用户信息', 'request': {'method': 'get', 'url': 'http://localhost:8888/users/2'}, 'validate': None}
    # print(verify_yaml(a))
    a = read_testcase("../test_api/test_project_generate/test_project.yaml")
    b = yaml.safe_dump(a)
    print( b)
    print(type( b))