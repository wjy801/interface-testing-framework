import requests
from commons.log import logger




# 统一请求封装
class RequestUtil:
    sess = requests.session()

    def send_all_request(self,**kwargs):

        for key,value in kwargs.items():
            # 对参数进行处理
            try:
                # 对文件上传路径进行处理
                if key == "files":
                    for file_key,file_value in value.items():
                        value[file_key] = open(file_value,mode="rb")
            except Exception:
                logger.error("文件上传路径错误")
            # 请求四要素写入日志
            logger.info("请求"+key+"参数:%s"%value)
        # 发送请求
        res = RequestUtil.sess.request(**kwargs)
        # 判断返回的内容是否是一个json格式
        if "json" in res.headers.get("Content-Type"):
            logger.info("响应内容:%s"%res.json())
        else:
            logger.info("响应内容不做书写")
        return res
if __name__ == '__main__':
    requests.get()
