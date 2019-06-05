"""
每个不同集合的API获取方式
"""
import os
from dump import class_dump_utils
from api import api_helpers

from itertools import groupby

# SET_A dump framework所有的API，Mach-o文件导出对应头文件
def frame_work_dump_apis(version, framework_folder):
    """
    class-dump framework下库生成的所有头文件api
    :param version:  SDK版本
    :param framework_folder: 公有framework的路径
    :return:
    """
    # dump 目标文件的framework到指定目录 /tmp/public_headers/xxx.framework/Headers/xxx.h  返回值 /tmp/public-headers/ 打成.h
    framework_header_path = __class_dump_frameworks(framework_folder, 'public_headers/')

    # 获取.h文件集合
    all_headers = __get_headers_from_path(framework_header_path)

    # 解析文件内容，获得api
    framework_apis = __get_apis_from_headers(version, all_headers)

    return framework_apis



# 用class-dump 分析framework目录 将.h文件输出到对应的目录  返回Folder   /tmp/public-headers
def __class_dump_frameworks(folder, prefix):
    current_dir = os.getcwd()
    header_folder_path = os.path.join(current_dir + '/tmp/' + prefix) # /tmp/public-headers

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
                all_headers_path += iterate_dir(framework, "", os.path.join(framework, header_path))
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
            files += iterate_dir(framework, prefix + f + "/", os.path.join(path,f))
    return files


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













































