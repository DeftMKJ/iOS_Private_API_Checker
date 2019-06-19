import random
import datetime
import time
import os
import zipfile
import subprocess
from macholib import MachO, mach_o


def unzip_ipa(ipa_path, desc_path):
    """
    解压ipa 到指定目录 返回zip folder
    """
    if not zipfile.is_zipfile(ipa_path):
        print('不存在压缩文件ipa')
        return None

    # 解压到指定目录 tmp
    file_zip = zipfile.ZipFile(ipa_path, 'r')
    file_zip.extractall(desc_path)
    file_zip.close()

    return os.path.join(desc_path, 'Payload')


def get_executable_file(path):
    """
    从ipa中解压出Payload目录中的 xxxx.app，扫描其中文件，寻找到Mach-O文件的路径 剔除Framework，拿出第一个可执行文件
    """
    cmd = u'python -mmacholib find %s'%path
    out_put = subprocess.check_output(cmd, shell=True).decode('utf-8')
    if out_put:
        out_put = out_put.split()
        if out_put and len(out_put) > 0:
            return os.path.join(path, out_put[0])
    return False


def check_architetures(app):
    """
    架构检查  arm64  arm7  arm7s  i386 x864

    以下是支付SDK的
    ['ARM_CPU_SUBTYPE_ARM_V7_32-bit', 'ARM64_CPU_SUBTYPE_ARM64_ALL_64-bit']
    """
    m = MachO.MachO(app)
    archs = []
    for header in m.headers:
        if header.MH_MAGIC == mach_o.MH_MAGIC_64 or header.MH_MAGIC == mach_o.MH_CIGAM_64:
            sz = '64-bit'
        else:
            sz = '32-bit'

        arch = mach_o.CPU_TYPE_NAMES.get(header.header.cputype, header.header.cputype)
        subarch = mach_o.get_cpu_subtype(header.header.cputype, header.header.cpusubtype)

        archs.append('_'.join((arch, subarch, sz)))

    return archs


def check_app_strings(app_exe):
    """
    Mach-O file in app path
    返回可执行文件中字符串
    strings 显示app中可打印字符
    strings 主要用于是确定非文本文件的包含的文本内容
    """
    cmd = u'/usr/bin/strings %s'%app_exe
    output = subprocess.check_output(cmd.split())
    return set(output.decode('utf-8').split())













# 获取随机值
def get_digest_str():
    datetime_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
    return datetime_str + '-' + str(datetime.datetime.now().microsecond) + '-' + str(random.randint(0, 1000))


if __name__ == '__main__':
    # unzip_ipa('/Users/mikejing191/Desktop/SmartPay_Example-IPA/SmartPay_Example-v1.3.2-b20190610182937.ipa', '/Users/mikejing191/Desktop/T2')

    app_exe = '/Users/mikejing191/Desktop/SmartPay_Example-IPA/Payload/SmartPay_Example.app/SmartPay_Example'

    archs = check_architetures(app_exe)
    print(archs)
    # print(check_app_strings(app_exe))