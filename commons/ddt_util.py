import json

import yaml


def read_testcase(yaml_path):
    with open(yaml_path,encoding="utf-8") as f:
        case_list = yaml.safe_load(f)
        if len(case_list)>=2:
            return [case_list]
        else:
            if "parametrize" in dict(*case_list).keys():
                new_caseinfo = ddts(*case_list)
                return new_caseinfo
            else:
                return case_list


def ddts(caseinfo: dict):
    data_list = caseinfo["parametrize"] # 二维数组
    len_flag = True
    name_len = len(data_list[0]) # 获取参数名长度
    for data in data_list:
        if len(data) != name_len: # 判断参数长度是否都一致
            len_flag = False
            print("parametrize参数长度不一致")
            break

    # 将字典转换成yaml字符串
    str_caseinfo = yaml.dump(caseinfo)
    new_caseinfo = []
    if len_flag:
        for x in range(1,len(data_list)): # x表示行，从下标为1开始
            raw_caseinfo = str_caseinfo
            for y in range(0,name_len): # y表示列，从下标为0开始
                if isinstance(data_list[x][y],str) and data_list[x][y].isdigit(): # 判断是否为数字字符串
                    data_list[x][y] = "'"+data_list[x][y]+"'"
                # 将需要参数化的值，替换为data_list[x][y]
                raw_caseinfo = raw_caseinfo.replace("$ddt{"+data_list[0][y]+"}",str(data_list[x][y]))
            # 将yaml字符串转换成字典
            case_dict = yaml.safe_load(raw_caseinfo)
            # 删除parametrize键值对
            case_dict.pop("parametrize")
            # 将参数化后的用例，按照行的顺序，批量添加到列表中
            new_caseinfo.append(case_dict)
    return new_caseinfo
if __name__ == '__main__':
    def read_testcase(yaml_path):
        with open(yaml_path, encoding="utf-8") as f:
            case_list = yaml.safe_load(f)
            if len(case_list) >= 2:
                return [case_list]
            else:
                if "parametrize" in dict(*case_list).keys():
                    a = dict(*case_list)
                    b = json.dumps(a)
                    print( b)
                    return None

                else:
                    return case_list
    a = read_testcase("../test_api/test_project_generate/b.yaml")
    print(a)