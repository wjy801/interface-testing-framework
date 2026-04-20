import yaml

from config import setting


def read_yaml(key):
    with open(setting.extract_file,encoding="utf-8") as f:
        value = yaml.safe_load(f)
        return value[ key]

# 读取yaml当中的所有值
def read_all():
    with open(setting.extract_file,encoding="utf-8") as f:
        value = yaml.safe_load(f)
        return value

def write_yaml(data):
    with open(setting.extract_file, "a+", encoding="utf-8") as f:
        yaml.safe_dump(data, f,allow_unicode= True)

def clear_yaml():
    with open(setting.extract_file, "w", encoding="utf-8") as f:
        pass

def read_testcase(file_path):
    with open(file_path, encoding="utf-8") as f:
        value = yaml.safe_load(f)
        return value

if __name__ == '__main__':
    # print(read_testcase("../test_api/test_project_generate/b.yaml"))


    def read_testcase(yaml_path):
        with open(yaml_path, encoding="utf-8") as f:
            case_list = yaml.safe_load(f)
            if len(case_list) >= 2:
                print("流程用例,[{},{},{}]")
                return [case_list]
            else:
                print("单用例或数据驱动,[{}]")
                if "parametrize" in dict(*case_list).keys():
                    print("数据驱动用例")
                    print(type(*case_list))
                    print(case_list)
                    print(*case_list)
                    new_caseinfo = ddts(*case_list)
                    return new_caseinfo
                else:
                    print("单用例")
                    return case_list


    def ddts(caseinfo: dict):
        data_list = caseinfo["parametrize"]
        len_flag = True
        name_len = len(data_list[0])  # 获取参数名长度
        for data in data_list:
            if len(data) != name_len:  # 判断参数长度是否都一致
                len_flag = False
                print("parametrize参数长度不一致")
                break
    read_testcase("../test_api/test_project_generate/b.yaml")
