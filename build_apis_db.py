import os
from config import sqlite3_info, db_names
from db_helper import create_dbs, api_dbs
from config import sdks_configs
from api import api_utils


import sys


def rebuild_sdk_private_apis(sdk_info):
    print("*"*100)
    print('SET_A')
    print(rebuild_dump_framework_api(sdk_info['sdk_version'], sdk_info['framework_path']))
    print("*" * 100)

    print("*" * 100)
    print('SET_B')
    print(rebuild_framework_header_api(sdk_info['sdk_version'], sdk_info['framework_header_path']))
    print("*" * 100)

    print("*" * 100)
    print('SET_C')
    print(rebuild_document_api(sdk_info['sdk_version'], sdk_info['docset_path']))
    print("*" * 100)

    print("*" * 100)
    print('SET_E')
    print(rebuild_private_dump_framework_api(sdk_info['sdk_version'], sdk_info['private_framework_path']))
    print("*" * 100)

    print("*" * 100)
    print('SET_D')
    print(rebuild_private_apis(sdk_info['sdk_version']))
    print("*" * 100)

def rebuild_dump_framework_api(sdk_version, framework_folder):
    """
    public-framework-dump-apis
    SET_A
    :param sdk_version: 版本
    :param framework_folder: public路径
    """
    table_name = db_names['SET_A']
    # 先清除已有版本的api
    api_dbs.delete_api_by_sdk_version(table_name, sdk_version)
    framework_dump_header_apis = api_utils.frame_work_dump_apis(sdk_version, framework_folder)

    # [{'class':'','methods':'','type':''},{},{}]
    return api_dbs.insert_apis(table_name, framework_dump_header_apis)


def rebuild_framework_header_api(sdk_version, framework_folder):
    """
    public-framework-.h-apis
    SET_B
    """
    table_name = db_names['SET_B']
    api_dbs.delete_api_by_sdk_version(table_name, sdk_version)

    framework_header_apis = api_utils.framework_header_apis(sdk_version, framework_folder)

    # [{'class':'','methods':'','type':''},{},{}]
    return api_dbs.insert_apis(table_name, framework_header_apis)

def rebuild_document_api(sdk_version, docset):
    """
    document api
    SET_C
    """
    table_name = db_names['SET_C']
    api_dbs.delete_api_by_sdk_version(table_name, sdk_version)
    document_apis = api_utils.document_apis(sdk_version, docset)

    return api_dbs.insert_apis(table_name, document_apis)

def rebuild_private_dump_framework_api(sdk_version, framework_folder):
    """
    private_framework_dump_apis
    SET_E
    """
    table_name = db_names['SET_E']
    api_dbs.delete_api_by_sdk_version(table_name, sdk_version)
    private_framework_dump_apis = api_utils.deduplication_api_list(api_utils.private_framework_dump_apis(sdk_version, framework_folder))

    return api_dbs.insert_apis(table_name, private_framework_dump_apis)

# 组合获取所有的私有API库
def rebuild_private_apis(sdk_version):


    table_name_D = db_names['SET_D'] # 最终的私有API
    table_name_F = db_names['SET_F'] # public 下过滤出来的私有API

    # flush table datas
    api_dbs.delete_api_by_sdk_version(table_name_D, sdk_version)
    api_dbs.delete_api_by_sdk_version(table_name_F, sdk_version)

    # public下私有API
    framework_dump_private_apis = []
    # public下所有API
    framework_dump_apis = api_dbs.get_publick_framework_dump_apis(sdk_version)

    public_count = 0
    private_count = 0
    __count = 0
    for api in framework_dump_apis:
        print("正在从公有API库中提取私有API-->%s"%api)
        # 方法以 '_'下划线开始直接定义为私有API
        if api['api_name'] and api['api_name'][0:1] == "_":
            __count += 1
            framework_dump_private_apis.append(api)
            continue
        # 不以下划线开头
        # 属于头文件
        is_header = api_dbs.api_is_exist_in_table(db_names['SET_B'], api)
        if is_header:
            public_count += 1
        else:
            # 属于文档
            is_doc = api_dbs.api_is_exist_in_table(db_names['SET_C'], api)
            if is_doc:
                public_count += 1
            else:
                private_count += 1
                framework_dump_private_apis.append(api)
    print("*"*100)
    print("所有公有framework下的API计算如下:")
    print("属于公有%s"%public_count)
    print("属于私有%s"%private_count)
    print("属于私有下划线%s"%__count)
    print("*" * 100)
    # 属于公有11217
    # 属于私有98566
    # 属于私有下划线28292

    print("去重前---公有库内的私有API length：%s" % (len(framework_dump_private_apis)))
    print('start group by....')

    framework_dump_private_apis = api_utils.deduplication_api_list(framework_dump_private_apis)
    print("去重后----公有库内的私有API length：%s" % (len(framework_dump_private_apis)))


    public_private_resultA = api_dbs.insert_apis(table_name_D, framework_dump_private_apis)
    print("公有库下的私有API插入最终集合---%s---%s" % (table_name_D, public_private_resultA))

    public_private_resultB = api_dbs.insert_apis(table_name_F, framework_dump_private_apis)
    print("公有库下的私有API插入独立集合F集合---%s---%s" % (table_name_F, public_private_resultB))

    # 合并 SET_D
    private_framework_apis = api_dbs.get_private_framework_dump_apis(sdk_version)
    public_private_resultC = api_dbs.insert_apis(table_name_D, private_framework_apis)
    print("私有库API集合取出插入合并集合SET_D---%s---%s" % (table_name_D, public_private_resultC))

    return True


if __name__ == '__main__':
    if not os.path.exists(sqlite3_info['sqlite3']):
        print('sqlite3 db not exists, creating......')
        create_dbs.create_relate_tables()


    for sdk_info in sdks_configs:
        rebuild_sdk_private_apis(sdk_info)
