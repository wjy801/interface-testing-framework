import copy

import pymysql

from config import setting


class AssertUtil:

    # 连接数据库
    def conn_detabase(self):
        self.conn = pymysql.connect(
            host=setting.db_host,
            port=setting.db_port,
            user=setting.db_username,
            password=setting.db_password,
            database=setting.db_database,
            charset="utf8"
        )
        return self.conn

    # 执行SQL
    def execute_sql(self,sql):
        # 创建连接
        conn = self.conn_detabase()
        # 创建游标
        cs = conn.cursor()
        # 执行SQL
        cs.execute(sql)
        # 取值
        value = cs.fetchone()
        # 关闭连接
        cs.close()
        conn.close()
        return value

    # 断言封装
    def assert_all_case(self,res,assert_type,value):
        # 1.深拷贝一个res
        resp = copy.deepcopy( res)
        # 2.把json方法改成属性
        try:
            resp.json = resp.json()
        except Exception:
            resp.json = {"msg": "response not json data"}
        # 3.循环判断断言
        for msg,data in value.items():
            yq,sj =  data[0],data[1]
            # 根据反射获取属性的值
            try:
                sj_value = getattr(resp,sj)
                print("\n"+assert_type, msg, yq, sj_value)
            except Exception:
                sj_value = sj
            # 判断断言
            match assert_type:
                case "equals":
                    assert yq == sj_value,msg
                case "contains":
                    assert yq in sj_value,msg
                case "db_equals":
                    yq_value = self.execute_sql(yq)
                    assert yq_value[0] == sj_value,msg
                case "db_contains":
                    yq_value = self.execute_sql(yq)
                    assert yq_value[0] in sj_value,msg









if __name__ == '__main__':
    calue = AssertUtil().execute_sql("select name from user where id =3")
    print(calue[0])