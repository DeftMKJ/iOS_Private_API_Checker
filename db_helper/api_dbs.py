from db_helper.sqlite3_utils import SqliteHandler


def delete_api_by_sdk_version(table_name, version):
    sql = "delete from " + table_name + " where source_sdk = ?"
    print('删除早期版本apis')
    return SqliteHandler().execute_update(sql, params=(version,))

# (:api_name,:api_name,:api_name,:api_name,:api_name,:api_name)
def insert_apis(table_name, datas):
    """
    Mysql
    https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-executemany.html
    如果是 [(),(),()] 则用%s
    如果是[{},{},{}] 就用 :name取值
    """
    sql = "insert into " + table_name + " (api_name,class_name,type,header_file,source_sdk,source_framework) values (:api_name,:class_name,:type,:header_file,:source_sdk,:source_framework)"
    return SqliteHandler().insert_many(sql, datas)