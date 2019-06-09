"""
每个不同集合的API获取方式
"""
import os
from dump import class_dump_utils
from api import api_helpers
from db_helper import dsidx_dbs
from itertools import groupby

from itertools import groupby


# SET_A  dump framework所有的API，Mach-o文件导出对应头文件
def frame_work_dump_apis(version, framework_folder):
    """
    class-dump framework下库生成的所有头文件api
    """
    # dump 目标文件的framework到指定目录 /tmp/public_headers/xxx.framework/Headers/xxx.h  返回值 /tmp/public-headers/ 打成.h
    framework_header_path = __class_dump_frameworks(framework_folder, 'public_headers/')

    # 获取.h文件集合
    all_headers = __get_headers_from_path(framework_header_path)

    # 解析文件内容，获得api
    framework_apis = __get_apis_from_headers(version, all_headers)

    return framework_apis


# SET_B  framework  头文件所有API
def framework_header_apis(version, framework_folder):
    '''
    获取framework暴露出来的头文件所有apis
    '''
    all_headers = __get_headers_from_path(framework_folder)

    framework_apis = __get_apis_from_headers(version, all_headers)
    # print(framework_apis)

    return framework_apis


# SET_C DocumentSet文件下的API集合
def document_apis(version, dsidx_path):
    """
    /Users/mikejing191/Desktop/私有API学习/com.apple.adc.documentation.iOS.docset/Contents/Resources/docSet.dsidx.db
    获取docSet数据库中的文档API
    """
    doc_apis = []
    # 从dsidxdb中拿到我们需要的文档API
    apisets = dsidx_dbs.get_dsidx_apis(dsidx_path)
    # 过滤
    for api in apisets:
        print('正在处理dosset %s' % api)
        Z_PK = api['Z_PK']
        ZDECLAREDIN = api['ZDECLAREDIN']
        # TODO 这里很多是空的
        ZCONTAINER = api['ZCONTAINER']

        container_name = ''
        if Z_PK:
            container_name = dsidx_dbs.get_container_name(dsidx_path, ZCONTAINER) or ''

        framework_name = ''
        header_path = ''
        if ZDECLAREDIN:
            framework_header = dsidx_dbs.get_framework_and_header_name(dsidx_path, ZDECLAREDIN)
            if framework_header:
                framework_name = framework_header.get('ZFRAMEWORKNAME', '')
                header_path = framework_header.get('ZHEADERPATH', '')
        doc_apis.append({"api_name": api['ZTOKENNAME'], "class_name": container_name, "type": api['ZTOKENTYPE'],
                         "header_file": header_path, "source_sdk": version, "source_framework": framework_name, })

    return doc_apis


# SET_F 私有框架下的API集合
def private_framework_dump_apis(version, framework_folder):
    """
    private_framework下的API
    """
    framework_folder = __class_dump_frameworks(framework_folder, 'private_headers/')
    all_headers = __get_headers_from_path(framework_folder)
    framework_apis = __get_apis_from_headers(version, all_headers)
    return framework_apis


# 用class-dump 分析framework目录 将.h文件输出到对应的目录  返回Folder   /tmp/public-headers
def __class_dump_frameworks(folder, prefix):
    current_dir = os.getcwd()
    header_folder_path = os.path.join(current_dir + '/tmp/' + prefix)  # /tmp/public-headers

    # listdir() 列出所有文件
    for framework in os.listdir(folder):
        if framework.endswith('.framework'):
            # source
            framework_path = os.path.join(folder, framework)
            # destination  /tmp/pub-headers/xxx.framework/Headers/
            out_path = os.path.join(os.path.join(header_folder_path + framework), 'Headers')
            class_dump_utils.dump_framework(framework_path, out_path)
    return header_folder_path


# 从dump的目录下获取所有的，获取所有的.h文件
def __get_headers_from_path(framework_folder):
    all_headers_path = []
    frameworks = os.listdir(framework_folder)
    for framework in frameworks:
        if framework.endswith('.framework'):
            header_path = os.path.join(os.path.join(framework_folder, framework), 'Headers')
            if os.path.exists(header_path):
                all_headers_path += iterate_dir(framework, "", header_path)
    # [('framework'),('headerfle'),('filepath')]
    return all_headers_path


# framwork   xxxx.framework
# prefix     ""
# path       tmp/public-header/xxxx.framework/Headers
def iterate_dir(framework, prefix, path):
    files = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            # ('xxxx.framework','xxx.h', '具体路径')
            files.append((framework, prefix + f, os.path.join(path, f)))
        elif os.path.isdir(os.path.join(path, f)):
            files += iterate_dir(framework, prefix + f + "/", os.path.join(path, f))
    return files


# 从头文件正则出来进行模型组装
def __get_apis_from_headers(sdk_version, all_headers):
    # 路径遍历(frameworkname, prefix, 具体路径)
    framework_apis = []
    for header in all_headers:
        # [{'class':'','methods':'','type':''},{},{}]
        apis = api_helpers.get_apis_from_header_file(header[2])

        for api in apis:
            class_name = api["class"] if api["class"] != "ctype" else header[1]
            method_list = api["methods"]
            m_type = api["type"]
            for m in method_list:
                tmp_api = {}
                tmp_api['api_name'] = m
                tmp_api['class_name'] = class_name
                tmp_api['type'] = m_type
                tmp_api['header_file'] = header[1]
                tmp_api['source_sdk'] = sdk_version
                tmp_api['source_framework'] = header[0]
                framework_apis.append(tmp_api)

    return framework_apis


# api去重 根据api_name和class_name
def deduplication_api_list(apis):
    """
    相同类名和相同方法名去重
    :param apis:
    :return:
    """

    def group_by_api(api):
        return api['api_name'] + '/' + api['class_name']

    new_apis = []

    # 先排序
    apis = sorted(apis, key=group_by_api)

    # 再根据类名和方法名成组
    for group, itr in groupby(apis, key=group_by_api):
        l = list(itr)
        if l and len(l) > 0:
            new_apis.append(l[0])

    return new_apis

# 案例如下，根据date排序，分组之后取出该组下第一个即可，那么上面是根据类名和方法名分组，去重取出第一个即可
# rows = [
#     {'address': '5412 N CLARK', 'date': '07/01/2012'},
#     {'address': '5148 N CLARK', 'date': '07/04/2012'},
#     {'address': '5800 E 58TH', 'date': '07/02/2012'},
#     {'address': '2122 N CLARK', 'date': '07/03/2012'},
#     {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
#     {'address': '1060 W ADDISON', 'date': '07/02/2012'},
#     {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
#     {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
# ]
# def group_by_date(obj):
#     return obj['date']
# x = sorted(rows, key=group_by_date)
#
# [{'address': '5412 N CLARK', 'date': '07/01/2012'},
#  {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
#  {'address': '5800 E 58TH', 'date': '07/02/2012'},
#  {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
#  {'address': '1060 W ADDISON', 'date': '07/02/2012'},
#  {'address': '2122 N CLARK', 'date': '07/03/2012'},
#  {'address': '5148 N CLARK', 'date': '07/04/2012'},
#  {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}]
#
# y = groupby(x, group_by_date)
#
# for g, l in y:
#     print(g)
#     print(list(l)
#
# 07 / 01 / 2012
#     [{'address': '5412 N CLARK', 'date': '07/01/2012'}
#     {'address': '4801 N BROADWAY', 'date': '07/01/2012'}]
# 07 / 02 / 2012
#     [{'address': '5800 E 58TH', 'date': '07/02/2012'},
#      {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
#      {'address': '1060 W ADDISON', 'date': '07/02/2012'}]
# 07 / 03 / 2012
#     [{'address': '2122 N CLARK', 'date': '07/03/2012'}]
# 07 / 04 / 2012
#     [{'address': '5148 N CLARK', 'date': '07/04/2012'},
#      {'address': '1039 W GRANVILLE', 'date': '07/04/2012'}]
