import os, shutil
from api import app_utils, api_utils
from dump import otool_utils
from db_helper import api_dbs
from  private_apis_app.utils import checkipa
from utils import report_utils
from dump import codesign_utils
from private_apis_app.utils import checkipa
from pprint import pprint

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
    # print('dump_macho_result_strings:--->')
    # print(dump_macho_result)
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
    print("App协议，变量属性 : %s" % len(app_availables))
    print("剩下的字符串--->  String -  App协议，变量属性  : %s"%len(leave))
    print('App方法名app_methods: %s'%len(app_apis))
    print('App用的Public对应的private apis length :%s'%len(api_set))
    print("*"*50)

    # App可见Strings: 14634
    # 自定义的app_availables: 3954
    # 剩下的String - app_availables: 11640
    # App方法名app_methods: 4088
    # App用的Public对应的private
    # apis
    # length: 15125

    # app中leave（所有API除开自定义的）和用到的Public库对应的私有API集合进行交叉，获得App中私有API关键字数据 [{},{},{}]
    intersection_api = api_utils.intersection_leave_list_and_private_apis(leave, api_set)
    print('strings剩余可见字符串关键字和Publick对应的私有API集合交集后的私有API--->%s'%len(intersection_api))
    # print(intersection_api)

    methods_in_app, method_not_in = api_utils.intersection_api(app_apis, intersection_api)  # app中的私有方法

    print("*"*50)
    print("最终API扫描结果")
    print('method_in_app:%s'%(len(methods_in_app)))
    print('method_not_in_app:%s' % (len(method_not_in)))
    print('private framework:%s'%len(private))
    print("*" * 50)
    return methods_in_app, method_not_in, private



def check_one_app():
    # ipa文件所在位置
    ipa_path = "/Users/mikejing191/Desktop/SmartPay_Example-IPA/SmartPay_Example-v1.4.1-b20190703142838.ipa"

    # 打开文件
    privete_in_app = open("tmp/private_in_app.txt", "w")
    privete_not_in_app = open("tmp/private_not_in_app.txt", "w")

    # pid标识
    pid = app_utils.get_digest_str()
    print(pid)
    # 获取可执行文件
    app = get_executable_path(ipa_path, pid)
    print(app)
    # 架构扫描
    archs = chech_architectures(app)
    print(archs)
    # 私有API扫描
    a, b, c = check_private_api(app, pid)

    # 输出到临时文件txt
    print("*" * 50)
    print("Private Methods in Apps : %s" % len(a))
    for x in a:
        print(x)
        print(x, file=privete_in_app)
    privete_in_app.close()

    print("*" * 50)
    print("Private Methods not in Apps : %s" % len(b))
    print(b)
    for x in b:
        print(x)
        print(x, file=privete_not_in_app)
    privete_not_in_app.close()
    print("*" * 50)
    print("Private Frameworks in Apps : %s" % len(c))
    print("*" * 50)


def get_file_md5(ipa_path):
    return app_utils.file_md5(ipa_path)


# 该方法是2.7的，3x需要重写
def check_app_info_and_provision(ipa_path):
    return checkipa.process_ipa(ipa_path)


def check_ipa(ipa_path):
    results = {}
    pid = app_utils.get_digest_str()

    print('1.', "*" * 10, 'get_file_md5')
    results['md5'] = get_file_md5(ipa_path)


    print('2.', '*'*10, 'check_app_info_and_provision')
    infos = check_app_info_and_provision(ipa_path)
    pprint(infos)
    for key in infos.keys():
        print(key)
        results[key] = infos[key]

    print('3', '*'*10, 'check_private_api')
    app = get_executable_path(ipa_path, pid)
    if not app:
        return False

    methods_in_app, methods_not_in_app,private_framework = check_private_api(app, pid)
    print('查看下结构字段')
    print(methods_not_in_app)
    results['private_apis'] = methods_in_app
    results['private_frameworks'] = list(private_framework)


    print('4','*'*10, 'check_architecture:')
    arcs = chech_architectures(app)
    results['arcs'] = arcs
    if len(arcs) < 2:
        results['error'].append({'label': 'Architecture:',
                                'description': 'app may be not support 64-bit'})


    print('5', '*'*10, 'check_codesign_info:')

    codesigin =  codesign_utils.codesignapp(app)
    results['codesign'] = codesigin


    print("6", '*'*10, 'remove tmp file')
    cur_dir = os.getcwd()
    dest_tmp = os.path.join(cur_dir,'tmp/' + pid)
    if os.path.exists(dest_tmp):
        shutil.rmtree(dest_tmp)


    return results


def batch_check(ipa_folder, excel_path):
    if not ipa_folder or not excel_path:
        return False
    check_results = []
    for ipa in os.listdir(ipa_folder):
        if ipa.endswith('.ipa'):
            print('start check ipa %s' % ipa)
            ipa_path = os.path.join(ipa_folder, ipa)
            print(ipa_path)
            try:
                r = check_ipa(ipa_path)
                if r:
                    check_results.append(r)
            except Exception as e:
                print(e)
                continue
    # 将结果导出为Excel
    report_utils.excel_report(check_results, excel_path)
    return excel_path






if __name__ == '__main__':
    # 单个指定ipa扫描
    # check_one_app()

    cwd = os.getcwd()
    excel_path = os.path.join(cwd, 'tmp/' + app_utils.get_digest_str() + '.xlsx')
    print('Excel 导出路径：%s' % excel_path)
    ipa_folder = '/Users/mikejing191/Desktop/SmartPay_Example-IPA/'
    batch_check(ipa_folder, excel_path)