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

def get_finale_private_apis_count():
    sql = "SELECT * FROM %s;" % db_names['SET_D']
    para = ()
    return SqliteHandler().execute_select(sql, params=para)


# 从SET_D 私有API库里面查找api_name 而且framework不属于参数，而且不在白名单里面
def get_private_api_list(framework=None):
    framework_str = _get_sql_in_strings(framework) # in frameworks
    private_db_name = db_names["SET_D"]
    white_list_containers = _get_white_lists_results()
    # 有frame过滤条件s
    if framework_str:
        sql = "select * from %s group by api_name, class_name having source_framework in "%(private_db_name) + framework_str + " and api_name not in " + white_list_containers + ";"
        params = ()
    else:
        sql = "select * from %s group by api_name, class_name having api_name not in "%(private_db_name) + white_list_containers + ";"
        params = ()
    private_apis = SqliteHandler().execute_select(sql, params)
    print(sql)
    return private_apis


# 白名单里面的api_name in sql语句
def _get_white_lists_results():
    sql = "select api_name from %s group by api_name, class_name" % (db_names["SET_G"])
    params = ()
    white_lists_result = SqliteHandler().execute_select(sql, params)
    result_set = set()
    if white_lists_result and len(white_lists_result) > 0:
        for api_name in white_lists_result:
            result_set.add(api_name['api_name'])
    return _get_sql_in_strings(result_set)


# set()数据 {'','',''} 转换成 ('','','') sql用的语句
def _get_sql_in_strings(container_set):
    framework_str = '()'
    if container_set and len(container_set) > 0:
        framework_str = '('
        for f in container_set:
            framework_str = framework_str + "'" + f + "', "

        framework_str = framework_str[0:-2]
        framework_str = framework_str + ')'
    return framework_str