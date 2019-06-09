from db_helper.sqlite3_utils import SqliteHandler
from config import db_names


# flush table with sdk
def delete_api_by_sdk_version(table_name, version):
    sql = "delete from " + table_name + " where source_sdk = ?"
    print('删除早期版本apis')
    return SqliteHandler().execute_update(sql, params=(version,))

# (:api_name,:api_name,:api_name,:api_name,:api_name,:api_name)
# 多插
def insert_apis(table_name, datas):
    """
    Mysql
    https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-executemany.html
    如果是 [(),(),()] 则用%s
    如果是[{},{},{}] 就用 :name取值
    """
    sql = "insert into " + table_name + " (api_name,class_name,type,header_file,source_sdk,source_framework) values (:api_name,:class_name,:type,:header_file,:source_sdk,:source_framework)"
    return SqliteHandler().insert_many(sql, datas)


# 获取所有public framework下所有的api
def get_publick_framework_dump_apis(version):
    sql = "SELECT * FROM %s WHERE source_sdk = ?;" % db_names['SET_A']
    para = (version, )
    return SqliteHandler().execute_select(sql, params=para)

# 获取所有private framework下的所有api
def get_private_framework_dump_apis(version):
    sql = "SELECT * FROM %s WHERE source_sdk = ?;" % db_names['SET_E']
    para = (version,)
    return SqliteHandler().execute_select(sql, params=para)

def api_is_exist_in_table(table_name, api_obj):
    sql = "SELECT * FROM %s WHERE api_name = ? and class_name = ? and source_sdk = ?;" % table_name
    parameters = (api_obj['api_name'], api_obj['class_name'], api_obj['source_sdk'])
    return SqliteHandler().execute_select_one(sql, params=parameters)