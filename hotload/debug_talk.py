import base64
import hashlib
import time

import rsa
import yaml

from commons.base_url_util import read_ini
from config import setting


class DebugTalk:

    def env(self,key):
        return read_ini()[key]

    def read_yaml(self,key):
        with open(setting.extract_file, encoding="utf-8") as f:
            value = yaml.safe_load(f)
            return value[key]

    def add(self,a,b):
        a = int(a)
        b = int(b)
        return a+b

    def md5_encode(self,data):
        # 先把data转化成utf-8的编码格式
        data = str(data).encode("utf-8")
        # md5加密，哈希算法
        md5_value = hashlib.md5( data).hexdigest()
        return md5_value

    def base64_encode(self,data):
        # 先把data转化成utf-8的编码格式
        data = str(data).encode("utf-8")
        # base64加密
        base64_value = base64.b64encode( data).decode("utf-8")
        return base64_value

    def get_number(self):
        return str(int(time.time()))

    # 生成RSA的公钥和私钥
    def create_key(self):
        (public_key,private_key) = rsa.newkeys(1024)
        with open("./public.pem","w+") as f:
            f.write(public_key.save_pkcs1().decode())
        with open("./private.pem","w+") as f:
            f.write(private_key.save_pkcs1().decode())

    def rsa_encode(self,data):
        # 加载公钥
        with open("./public.pem","r") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read().encode())
        # 把data转换成utf-8的编码格式
        data = str(data).encode("utf-8")
        # 把字符串加密成字节类型，为了解决中文乱码问题
        byte_value = rsa.encrypt(data,public_key)
        # 把字节转化成字符串格式
        resa_value = base64.b64encode(byte_value).decode("utf-8")
        return resa_value


if __name__ == '__main__':
    print(DebugTalk().rsa_encode("123"))