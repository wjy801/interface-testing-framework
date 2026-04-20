import traceback

import pytest

from commons.assert_util import AssertUtil
from commons.extract_util import ExtractUtil
from commons.model_util import CaseInfo
from commons.requests_util import RequestUtil, logger


def stand_case_flow(caseinfo: CaseInfo):
    # 显示请求参数
    logger.info("模块>接口>用例:"+str(caseinfo.feature)+">"+str(caseinfo.story)+">"+str(caseinfo.title))
    # 使用提取的值,构建新的、完整的请求
    new_request = ExtractUtil().use_extract_value(caseinfo.request)
    # 发送请求
    res = RequestUtil().send_all_request(**new_request)
    # 请求之后得到响应之后取提取变量
    if caseinfo.extract:
        for key, value in caseinfo.extract.items():
            ExtractUtil().extract(res, key, *value)

    # 请求得到响应后，如果validate不为None，则需要断言
    try:
        if caseinfo.validate:
            for assert_type,value in ExtractUtil().use_extract_value(caseinfo.validate).items():
                AssertUtil().assert_all_case(res,assert_type,value)
            logger.info("断言成功\n")
        else:
            logger.warning("此用例没有断言\n")
            print("此用例没有断言")
    except Exception:
        logger.error("断言失败：%s\n"%str(traceback.format_exc())) # 添加失败消息

