import copy
import re
from string import Template

import jsonpath
import yaml

from commons.yaml_util import write_yaml, read_all
from hotload.debug_talk import DebugTalk


class ExtractUtil:

    # 解析提取变量
    # attr_name是属性名，expr是表达式，index是下标
    def extract(self,res,var_name,attr_name,expr: str,index):
        # 深拷贝
        new_res = copy.deepcopy(res)
        try:
            new_res.json = new_res.json()
        except Exception:
            new_res.json = {"msg":'response not json data'}
        # 通过反射获取属性的值
        data = getattr(new_res,attr_name)
        # 判断通过什么方式提取数据
        if expr.startswith("$"):
            lis = jsonpath.jsonpath(dict(data),expr)
        else:
            lis = re.findall(expr,data)
        # 通过下标取值
        if lis:
            var_value = lis[index]
            write_yaml({var_name:var_value})

    # 解析使用变量,把${acess_token}替换为从extract.yaml中获取的中间变量值
    def use_extract_value(self,request_data: dict):
        # 1.把字典转换为yaml字符串
        data_str = yaml.safe_dump(request_data)
        # 2.字符串替换,模板要求是字符串，替换数据要求是字典
        # new_request_data = Template(data_str).safe_substitute(read_all())
        # 2.使用热加载替换,返回字符串
        new_request_data = self.hotload_replace(data_str)
        # 3.把字符串还原成字典
        data_dict = yaml.safe_load(new_request_data)

        return data_dict

    def hotload_replace(self,data_str: str):
        # 定义正则匹配${}表达式
        # regexp = "\\$\\{(.*?)\\}"                  #匹配${number}
        regexp = "\\$\\{(.*?)\\((.*?)\\)\\}"       #匹配${函数名(参数)}
        fun_list = re.findall(regexp,data_str)
        for f in fun_list:
            if f[1] == "": # 没有参数
                new_value = getattr(DebugTalk(),f[0])()
            else: # 有参数
                new_value = getattr(DebugTalk(),f[0])(*f[1].split(","))
            if isinstance(new_value,str) and new_value.isdigit():
                new_value = "'"+new_value+"'"
            # 拼接旧的值
            old_value = "${"+f[0]+"("+f[1]+")}"
            # 把旧的表达式替换成新的值
            data_str = data_str.replace(old_value,str(new_value))
        return data_str

if __name__ == '__main__':
    data_str = {"method":"${read_yaml(number)}","url":"http://localhost:8888/users/${add(2,3)}"}
    lis = yaml.safe_dump(data_str)
    print("old:", lis)
    print("new:",ExtractUtil().hotload_replace(lis))
