# iOS_Private_API_Checker
### Version
1.iOS 12.1 Xcode10 以上

2.Python3.7

3.Django 2.2

### Complete
1.Public-Framework-API-Dump成`xxxx.h`头文件 并且写入`framework_dump_apis`表中


### 虚拟环境配置
建议用Pycharm


1.下载项目下来,用Pycharm打开，然后点击Pycharm --- Preference --- Project --- Project Interpreter配置虚拟环境

2.点击右边的齿轮，选择add，Virtualenv Environment --- New Environment 默认确定即可

3.打开Pycharm下面的Terminal，进入虚拟环境，安装依赖包

4.生成 `pip freeze > requirements.txt`  安装 `pip install -r requirements.txt`

5.然后`build_apis_db.py`文件可以单独跑，就会在项目主目录下生成一个`tmp`文件夹生成对应`framework`dump之后的头文件

6.最后自动会正则这些头文件，然后写入`mkj_private_apis.db`对应的表中进行后续匹配


### TODO
