import os
from pprint import pprint
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import time

from datetime import date
from datetime import datetime
import random
import shutil
import json
import check_private_apis

# Create your views here.
def index(request):
    # return render(request,'checkipa/index.html')
    return render(request, 'dumpapp/index_page.html')


allow_ext = ['ipa']

def upload(request):
    rst = {}
    pid = get_unique_str()
    ipa_path = None
    try:
        upload_file = request.FILES['file']
        fname = upload_file.name
        print("*"*10,'name')
        print(fname)
        print(pid)
        print(upload_file)
        suffix_name = fname.split('.')[-1]
        # 文件后缀名不对时，不做存储处理
        if not suffix_name in allow_ext:
            rst['success'] = 0
            rst['success'] = 'file ext is not allowed'
        else:
            # 为图片名称添加时间戳，防止不同文件同名
            fname = pid + '.' + suffix_name
            ipa_path = os.path.join(settings.MEDIA_ROOT, fname)
            print('+'*10)
            print(ipa_path)
            with open(ipa_path, 'wb') as ft:
                # 内存中图片读取
                for ct in upload_file.chunks():
                    # 写入
                    ft.write(ct)
            rst['success'] = 1
            rst['data'] = {}
            # 获得ipa信息
            print('1111111111')
            rsts = check_private_apis.check_app_info_and_provision(ipa_path)
            for key in rsts.keys():
                rst['data'][key] = rsts[key]
            # 检查ios私有api
            print('22222222222222')
            app = check_private_apis.get_executable_path(ipa_path, pid)
            print('22222222222222333333333')


            methods_in_app, methods_not_in_app, private = check_private_apis.check_private_api(app, pid)
            print('33333333333333')
            rst['data']['methods_in_app'] = methods_in_app
            rst['data']['private_framework'] = list(private)
            # 检查ipa 64支持情况
            arcs = check_private_apis.chech_architectures(app)
            rst['data']['arcs'] = arcs

    except Exception as e:
        print('卧槽死了')
        print(e)
        rst['success'] = 0
        rst['data'] = '检查失败，也许上传的包并非真正的ipa，或者系统出现错误！'

    if ipa_path and os.path.exists(ipa_path):
        os.remove(ipa_path)  # 删除上传的包

    cur_dir = os.getcwd()  # 删除检查临时目录
    dest_tmp = os.path.join(cur_dir, 'tmp/' + pid)
    if os.path.exists(dest_tmp):
        shutil.rmtree(dest_tmp)
    if rst == None:
        return {}
    print("+" * 10)
    print(json.dumps(rst, cls=KJJsonEncoder))
    print("+" * 10)
    return HttpResponse(json.dumps(rst, cls=KJJsonEncoder))



def upload_tmp(request):
    pprint('进来了')
    # 注意是FILES
    file = request.FILES['file']
    print("*"*10)
    print(file)
    # 全路径
    storepath = os.path.join(settings.MEDIA_ROOT, file.name)
    print(storepath)
    # with是不需要手动释放内存  ft指针
    with open(storepath, 'wb') as ft:
        # 内存中图片读取
        for ct in file.chunks():
            # 写入
            ft.write(ct)
    # 这里的staitc是标识setting文件下的路径，会自动拼接那个路径，你然后后面跟media/xxx.jpg即可
    # return HttpResponse('<img src="/static/media/%s" alt="">' % file.name)


def get_unique_str():
    datetime_str = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime())
    return datetime_str + '-' + str(datetime.now().microsecond) + '-' + str(random.randint(0, 1000))

class KJJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)