from django.urls import path, re_path
from . import views

app_name = 'dumpapp'

urlpatterns = [
    # 这里需要协定头和尾
    re_path(r'^$',views.index, name='index'),
    re_path(r'^ipa_upload/$', views.upload, name='upload'),
    re_path(r'^upload_tmp/$', views.upload_tmp, name='upload_tmp'),
]

