import subprocess
import re
from utils import utils


# 获取class-dump对用平台下的可执行文件
class_dump_path = utils.get_class_dump_path()
# 拼接class-dump cmd   ./clss-dump xxxx.framework -o ./Desktop/xxx
# dump_cmd = class_dump_path + " -H %s -o %s"
dump_cmd = class_dump_path + " -H %s -o %s"


# class-dump -H xxxx.frameworkpath -o xxxx.path  dump framework下的头文件
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

# 截取路径方法
def get_dump_framework_name(framework_path):
    try:
        paths = re.split(r'/', framework_path)
        return 'class-dump-%s'%paths[-1]
    except Exception as e:
        print('截取路径失败' + e)
        return framework_path


# class-dump xxxx.path 是直接dump可执行文件   例如ipa --- payload --- Mach-O 可执行文件
def dump_app(app_path):
    cmd = class_dump_path + " %s" % app_path
    result = subprocess.check_output(cmd.split())
    return result.decode('utf-8')


if __name__ == '__main__':
    res = dump_framework('/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/CoreSimulator/Profiles/Runtimes/iOS.simruntime/Contents/Resources/RuntimeRoot/System/Library/Frameworks/AudioUnit.framework', '/Users/mikejing191/Desktop/UIKIt')



# subprocess
"""
subprocess module介绍 http://blog.chinaunix.net/uid-26000296-id-4461522.html
1.subprocess.call 
subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False)
运行由args指定的命令，直到命令结束后，返回 返回码的属性值。
方式一
subprocess.call('ls -a'.split())
方式二
subprocess.call('ls -a', shell=True)

subprocess.call('exit 1', shell=True)  输出1 错误

总结 正确返回0 错误就非0 不会崩溃抛出异常


2.subprocess.check_all
如果返回码为零，则返回。否则，抛出 CalledProcessError异常。
CalledProcessError对象包含有返回码的属性值。
subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False)

subprocess.check_call('exit 1', shell=True)  报错抛出CalledProcessError异常异常

总结 正确返回0 错误就非0 会崩溃抛出异常


3.subprocess_check_output
 subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, universal_newlines=False)
 运行args定义的命令，并返回一个字符串表示的输出值。
 如果返回码为非零，则抛出 CalledProcessError异常。
 
 总结 正确返回结果值输出，错误check_all一样抛出异常
"""



# u r b
"""
u/U:表示unicode字符串 
不是仅仅是针对中文, 可以针对任何的字符串，代表是对字符串进行unicode编码。 
一般英文字符在使用各种编码下, 基本都可以正常解析, 所以一般不带u；但是中文, 必须表明所需编码, 否则一旦编码转换就会出现乱码。 
建议所有编码方式采用utf8

r/R:非转义的原始字符串 
与普通字符相比，其他相对特殊的字符，其中可能包含转义字符，即那些，反斜杠加上对应字母，表示对应的特殊含义的，比如最常见的”\n”表示换行，”\t”表示Tab等。而如果是以r开头，那么说明后面的字符，都是普通的字符了，即如果是“\n”那么表示一个反斜杠字符，一个字母n，而不是表示换行了。 
以r开头的字符，常用于正则表达式，对应着re模块。

b:bytes 
python3.x里默认的str是(py2.x里的)unicode, bytes是(py2.x)的str, b”“前缀代表的就是bytes 
"""