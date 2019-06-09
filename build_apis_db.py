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
    print('SET_F')
    print(rebuild_private_dump_framework_api(sdk_info['sdk_version'], sdk_info['private_framework_path']))
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
    SET_F
    """
    table_name = db_names['SET_F']
    api_dbs.delete_api_by_sdk_version(table_name, sdk_version)
    private_framework_dump_apis = api_utils.deduplication_api_list(api_utils.private_framework_dump_apis(sdk_version, framework_folder))

    return api_dbs.insert_apis(table_name, private_framework_dump_apis)


if __name__ == '__main__':
    if not os.path.exists(sqlite3_info['sqlite3']):
        print('sqlite3 db not exists, creating......')
        create_dbs.create_relate_tables()


    for sdk_info in sdks_configs:
        rebuild_sdk_private_apis(sdk_info)
