import os
from pathlib import Path

import allure
import pytest

from commons.ddt_util import read_testcase
from commons.main_util import stand_case_flow
from commons.model_util import verify_yaml
from commons.requests_util import logger


@allure.epic("项目名称：wjy的接口测试")
class TestAllCase:
    pass


def collect_yaml_cases():
    testcase_path = Path(__file__).parent
    project_path = testcase_path.parent
    case_target = os.getenv("CASE_TARGET", "").strip()

    if not case_target:
        yaml_case_list = list(testcase_path.glob("*/*.yaml"))
        yaml_case_list.sort()
        return yaml_case_list

    target_path = Path(case_target)
    candidate_paths = []
    if target_path.is_absolute():
        candidate_paths.append(target_path)
    else:
        candidate_paths.append(testcase_path / target_path)
        candidate_paths.append(project_path / target_path)

    resolved_path = None
    for candidate_path in candidate_paths:
        if candidate_path.exists():
            resolved_path = candidate_path
            break

    if resolved_path is None:
        raise FileNotFoundError(f"未找到要执行的目录或文件: {case_target}")

    if resolved_path.is_file():
        return [resolved_path]

    yaml_case_list = list(resolved_path.glob("*.yaml"))
    yaml_case_list.sort()
    return yaml_case_list

# 根据一个yaml的路径创建一个测试用例的函数并且返回这个函数
def create_testcase(yaml_path):

    @pytest.mark.parametrize("caseinfo", read_testcase(yaml_path))
    def func(self,caseinfo):
        global case_obj
        if isinstance(caseinfo, list):
            logger.info("YAML测试用例路径"+str(yaml_path))# 流程用例
            for case in caseinfo:
                # 校验yaml中的请求四要素
                case_obj = verify_yaml(case,yaml_path)
                # 用例标准化流程
                stand_case_flow(case_obj)
        else: # 单接口用例
            logger.info("YAML测试用例路径" + str(yaml_path))
            # 校验yaml中的请求四要素
            case_obj = verify_yaml(caseinfo,yaml_path)
            # 用例标准化流程
            stand_case_flow(case_obj)
        # 定制allure报告
        allure.dynamic.feature(case_obj.feature)
        allure.dynamic.story(case_obj.story)
        allure.dynamic.title(case_obj.title)
    return func

# 循环获取所有的yaml文件（一个yaml生成一个用例，然后把用例放到类下面）
yaml_case_list = collect_yaml_cases()
for yaml_path in yaml_case_list:
    func = create_testcase(yaml_path)
    # 通过反射，这个循环每循环一次就生成一个yaml测试用例函数，把生成的函数加入到TestAllCase类下面
    setattr(TestAllCase,"test_"+yaml_path.stem,func)
