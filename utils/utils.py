import os, sys
import time
import datetime
import random
from config import class_dump_z_path


def get_system():
    """
    通过不同的操作系统匹配对应
    :return: 操作系统标识
    """
    system_platform = sys.platform
    if system_platform.startswith('linux'):
        return 'linux'
    elif system_platform.startswith('win32'):
        return 'win'
    elif system_platform.startswith('darwin'):
        return 'mac'
    else:
        return 'iphone'


def get_class_dump_path(use_what = 'class-dump'):
    if use_what == 'class-dump':
        # 项目根目录下的class-dump
        return os.path.join(os.getcwd() + '/class-dump')
    else:
        return class_dump_z_path.get(get_system(), os.path.join(os.getcwd() + 'class-dump'))


# 获取随机值
def get_digest_str():
    datetime_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
    return datetime_str + '-' + str(datetime.datetime.now().microsecond) + '-' + str(random.randint(0, 1000))