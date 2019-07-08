import random
import datetime
import time
import os
import zipfile
import subprocess
import re
from macholib import MachO, mach_o
from dump import class_dump_utils
from api import api_helpers
from hashlib import md5



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

        archs.append('_'.join((arch, sz)))

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


def get_dump_macho_result(app_path):
    """
     dump app 可执行文件
    """
    result = class_dump_utils.dump_app(app_path)
    return result



# @interface SPYConnectAccountVModel : SPYTableVModel
# {
#     unsigned long long _status;
#     SPYWalletBalanceEntityList *_balanceList;
#     NSString *_bankName;
#     NSString *_bankID;
#     unsigned long long _availability;
# }
# @interface SPYConnectAccountVModel ()
#
# @property (nonatomic, strong) SPYWalletBalanceEntityList *balanceList;
# @property (nonatomic, copy) NSString *bankName;
# @property (nonatomic, copy) NSString *bankID;
# @property (nonatomic, assign) SPYAccountAvailability availability;
#
# @end

# @interface SPYURLSessionManagerTaskDelegate : NSObject <NSURLSessionTaskDelegate, NSURLSessionDataDelegate, NSURLSessionDownloadDelegate>
# {
#     SPYURLSessionManager *_manager;
#     NSMutableData *_mutableData;
#     NSProgress *_uploadProgress;
#     NSProgress *_downloadProgress;
#     NSURL *_downloadFileURL;
#     CDUnknownBlockType _downloadTaskDidFinishDownloading;
#     CDUnknownBlockType _uploadProgressBlock;
#     CDUnknownBlockType _downloadProgressBlock;
#     CDUnknownBlockType _completionHandler;
# }
#
# @property(copy, nonatomic) CDUnknownBlockType completionHandler; // @synthesize completionHandler=_completionHandler;
# @property(copy, nonatomic) CDUnknownBlockType downloadProgressBlock; // @synthesize downloadProgressBlock=_downloadProgressBlock;
# @property(copy, nonatomic) CDUnknownBlockType uploadProgressBlock; // @synthesize uploadProgressBlock=_uploadProgressBlock;
# @property(copy, nonatomic) CDUnknownBlockType downloadTaskDidFinishDownloading; // @synthesize downloadTaskDidFinishDownloading=_downloadTaskDidFinishDownloading;
# @property(copy, nonatomic) NSURL *downloadFileURL; // @synthesize downloadFileURL=_downloadFileURL;
def get_app_available(dump_result, pid):
    """
    处理dump出来的 property  protocol以及class
    interface 类名
    protocol 协议名
    private m文件私有属性
    prop    property属性
    """

    # for x in dump_result.split('\n'):
    #     print(x)

    interface = re.compile("^@interface (\w*).*")
    protocol = re.compile("@protocol (\w*)")

    # NSObject < OS_dispatch_group >*_waitGroup; id <SEWebSocketDelegate> _delegate;
    # NSRunLoop *_runLoop;
    # unsigned char _currentReadMaskKey[4];
    # @interface SEWebSocket : NSObject <NSStreamDelegate> 案例
    private = re.compile("^\s*[\w <>]* [*]?(\w*)[\[\]\d]*;")  # m文件私有的变量
    prop = re.compile("@property\([\w, ]*\) (?:\w+ )*[*]?(\w+); // @synthesize \w*(?:=([\w]*))?;")  # 属性

    res = set()
    lines = dump_result.split("\n")
    wait_end = False
    for line in lines:
        l = line.strip()
        if l.startswith("}"):
            wait_end = False
            continue
        if wait_end:
            r = private.search(l)
            if r:
                res.add(r.groups()[0])
            continue
        r = interface.search(l)
        if r:
            res.add(r.groups()[0])
            wait_end = True
            continue
        r = protocol.search(l)
        if r:
            res.add(r.groups()[0])
            wait_end = True
            continue
        r = prop.search(l)
        if r:
            m = r.groups()
            res.add(m[0])
            res.add("set" + m[0].title() + ":")
            # print ("set" + m[0].title() + ":")
            if m[1] != None:
                # res.add("V"+m[1])
                res.add(m[1])
    return res




def get_app_methods(dump_result, pid):
    """
    获取App中的方法
    """
    methods = api_helpers.extract(dump_result)
    return methods




def file_md5(ipa_path):
    m = md5()
    with open(ipa_path, 'rb') as f:
        text = f.read()
        m.update(text)
        return m.hexdigest()
    return ''


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