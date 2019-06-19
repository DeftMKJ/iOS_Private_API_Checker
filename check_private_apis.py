import os
from api import app_utils
from dump import otool_utils

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
    # 获取App内一些可打印的文本信息 strings
    strings = app_utils.check_app_strings(app)

    # 获取App内私有库和公有库
    private, public = otool_utils.otool_app(app)

    print("="*20)
    print('private ' + str(len(private)))
    print('public ' + str(len(public)))
    print("=" * 20)



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
