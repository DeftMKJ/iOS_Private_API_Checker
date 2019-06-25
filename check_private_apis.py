import os
from api import app_utils, api_utils
from dump import otool_utils
from db_helper import api_dbs

# ipa路径 pid唯一标识 解压ipa包到项目tmp目录下 拿到可执行文件
def get_executable_path(ipa_path, pid):
    if not os.path.exists(ipa_path):
        return False

    cur_dir = os.getcwd()
    dest = os.path.join(cur_dir, 'tmp/' + pid)
    print(cur_dir)
    print(dest)
    if not os.path.exists(dest):
        os.mkdir(dest)
    app_path = app_utils.unzip_ipa(ipa_path, dest) or ''
    app_exe = app_utils.get_executable_file(app_path)
    return app_exe


# 提取架构
def chech_architectures(app_exe):
    archs = app_utils.check_architetures(app_exe)
    return archs


# 检查私有api 返回三个参数
def check_private_api(app, pid):
    # 获取App内一些可打印的文本信息 cmd:strings
    strings = app_utils.check_app_strings(app)

    print('Strings:--->')
    print(strings)

    # 获取App内私有库和公有库  cmd: otool -L
    private, public = otool_utils.otool_app(app)

    print("="*20)
    print('private ' + str(len(private)))
    print('public ' + str(len(public)))
    print("=" * 20)

    # class-dump ipa mach-o
    dump_macho_result = app_utils.get_dump_macho_result(app)
    print('dump_macho_result_strings:--->')
    print(dump_macho_result)
    app_availables = app_utils.get_app_available(dump_macho_result, pid) # 提取App自定义的方法 不需要检查 TODO 再仔细看下输出
    print('app_availables:--->')
    print(app_availables)

    leave = strings - app_availables # 去除一些App自定义的方法，剩余App中的一些字符串

    ### app_methods
    app_methods = app_utils.get_app_methods(dump_macho_result, pid) # class-dump出来的字符串格式中提取方法
    # [{"class": "ctype", "methods": method, "type": "C/C++"}]
    print("app_methods")
    print(app_methods)

    app_apis = []
    for m in app_methods:
        class_name = m['class'] if m['class'] != 'ctype' else 'cur_app'
        method_lists = m['methods']
        m_type = m['type']
        for m in method_lists:
            tmp_api = {}
            tmp_api['api_name'] = m
            tmp_api['class_name'] = class_name
            tmp_api['type'] = m_type
            app_apis.append(tmp_api)
    ### app_methods

    # Pulic用到的库中对应的私有API [{},{},{}]
    api_set = api_dbs.get_private_api_list(public)  # 数据库中的私有api，去除了whitelist白名单

    print("*"*50)
    print("App可见Strings : %s" % len(strings))
    print("自定义的app_availables : %s" % len(app_availables))
    print("剩下的String -  app_availables : %s"%len(leave))
    print('App方法名app_methods: %s'%len(app_apis))
    print('App用的Public对应的private apis length :%s'%len(api_set))
    print("*"*50)
    # Leave app_availables: 11640
    # app_methods: 4088
    # private length: 14938

    # app中leave（所有API除开自定义的）和用到的Public库对应的私有API集合进行交叉，获得App中私有API关键字数据 [{},{},{}]
    intersection_api = api_utils.intersection_leave_list_and_private_apis(leave, api_set)

    methods_in_app, method_not_in = api_utils.intersection_api(app_apis, intersection_api)  # app中的私有方法

    print("*"*50)
    print('method_in_app:%s'%(len(methods_in_app)))
    print('method_not_in_app:%s' % (len(method_not_in)))
    print('private framework:%s'%len(private))
    print("*" * 50)
    return methods_in_app, method_not_in, private





if __name__ == '__main__':
    ipa_path = "/Users/mikejing191/Desktop/SmartPay_Example-IPA/SmartPay_Example-v1.3.2-b20190610182937.ipa"

    pid = app_utils.get_digest_str()
    print(pid)
    app = get_executable_path(ipa_path, pid)
    print(app)
    archs = chech_architectures(app)
    print(archs)
    result = check_private_api(app, pid)
    print(result)
