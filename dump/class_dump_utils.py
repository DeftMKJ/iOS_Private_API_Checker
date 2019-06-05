import subprocess
import re
from utils import utils


# 获取class-dump对用平台下的可执行文件
class_dump_path = utils.get_class_dump_path()
# 拼接class-dump cmd   ./clss-dump xxxx.framework -o ./Desktop/xxx
# dump_cmd = class_dump_path + " -H %s -o %s"
dump_cmd = "class-dump" + " -H %s -o %s"

def dump_framework(framework_path, out_path):
    """
    使用class-dump来解析framework中的api
    """
    cmd = dump_cmd % (framework_path, out_path)
    print('~'*100)
    print(get_dump_framework_name(framework_path))
    result_code = subprocess.call(cmd.split())
    # 0代表执行成功
    if result_code != 0:
        print("class-dump error---> %s"%(get_dump_framework_name(framework_path)))
        print('~' * 100)
        return "class-dump error---> %s"%framework_path
    return ''

def get_dump_framework_name(framework_path):
    try:
        paths = re.split(r'/', framework_path)
        return 'class-dump-%s'%paths[-1]
    except Exception as e:
        print('截取路径失败' + e)
        return framework_path


if __name__ == '__main__':
    res = dump_framework('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/CoreSimulator/Profiles/Runtimes/iOS.simruntime/Contents/Resources/RuntimeRoot/System/Library/Frameworks/AudioUnit.framework', '/Users/mikejing191/Desktop/UIKIt')


