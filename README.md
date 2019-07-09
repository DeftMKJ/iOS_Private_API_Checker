## 前言
网上有个2.7 Python的资料，顺便熟练下Python，用Python3.7 + Django重写了一下，把Bug都修复了一下，慢慢完善
[网易游戏](https://github.com/NetEaseGame/iOS-private-api-checker)


# iOS_Private_API_Checker
### Version
1.iOS 12.1 Xcode10 以上

2.Python3.7

3.Django 2.2.3

### Complete
1.从ipa中提取一些基本信息，例如app名字，sdk版本，包名等，可以辅助QA日常工作。<br/>
2.ipa架构检查，可以看出是否支持64位架构，可以辅助AppStore提审
3.ipa使用私有api情况，可以辅助AppStore提审
4.mkj_private_apis.db已经是编译好的各种api集合，云盘地址（稍后提供），下载下来放进根目录，不然你自己要跑半个多小时才能全部入库

### 依赖
```ruby
altgraph==0.16.1
Django==2.2.3
macholib==1.11
pytz==2019.1
sqlparse==0.3.0
virtualenv==16.6.0
XlsxWriter==1.1.8
```


### 虚拟环境配置
virtualenv
1.进入项目文件夹，用virtualenv创建虚拟环境，没有该工具用pip install virtualenv / pip3 install virtualenv 安装
2.virtualenv venv
3.virtualenv -p /usr/local/bin/python3 venv # 创建3的环境
4.pip install -r requirements.txt  # 虚拟环境导入依赖
5.. venv/bin/activate  # 启动虚拟环境


Pycharm
1.下载项目下来,用Pycharm打开，然后点击Pycharm --- Preference --- Project --- Project Interpreter配置虚拟环境<br/>
2.点击右边的齿轮，选择add，Virtualenv Environment --- New Environment 默认确定即可<br/>
3.打开Pycharm下面的Terminal，进入虚拟环境，安装依赖包<br/>
4.生成 `pip freeze > requirements.txt`  安装 `pip install -r requirements.txt`<br/>
5.然后`build_apis_db.py`文件可以单独跑，就会在项目主目录下生成一个`tmp`文件夹生成对应`framework`dump之后的头文件<br/>
6.最后自动会正则这些头文件，然后写入`mkj_private_apis.db`对应的表中进行后续匹配<br/>

### 运行
#### 方式1
如果你会自己编译入库，就在`config.py`文件中找到`sdks_configs`，配置对应的路径地址，稍后博客有介绍如何配置，如果你想用线程的，就直接去云盘下载我编译好的iOS 12的api，但是docset是9.2.5的，直接把下载好的db文件拖进项目根目录即可，然后到根目录`check_private_apis.py`文件,修改main里面的check_multi(path),这里的path填写你的ipa所在文件夹,注意是文件夹，脚本会批量扫描目录下所有ipa并输出Excel，可以在项目tmp目录中找到生成的Excel文件

#### 方式2
刚才上面配置好的Django的虚拟环境，安装好了依赖，依然在项目根目录下，执行 `python private_apis_app/manage.py runserver` 启动本地服务，输入`http://127.0.0.1:8000/check/`,拖入你的ipa即可

### 小工具
[脚本检查ipa各种参数信息](https://github.com/DeftMKJ/iOS_Check_IPA_Details) Python3实现的，里面也有个Python2的


### 步骤原理分析
1、通过`class-dump`导出`Frameworks`以及`PrivateFrameworks`中可执行文件的头文件，通过脚本提取方法分别为`SET_A`集合和`SET_E`集合
2、通过`Framework`中的Header文件夹下暴露的头文件进行提取，通过脚本提取方法设置为`SET_B`集合                      
3、找到Xcode内置的`com.apple.adc.documentation.iOS.docset`数据库(iOS 9.3之后修改了内置数据结构，后面介绍再介绍)，多表查询出对应的API，设置`SET_C`集合
4、那么`SET_F =（SET_A - SET_B - SET_C）`就是公有Framework下对应的私有API，设置为集合`SET_F`
5、原本B集合中的API就是私有库里面的，因此都不能被使用，则最终的私有API集合为`SET_D = SET_F + SET_E`
6、使用`class-dump`反编译ipa包中的app文件，然后和`SET_D`做交集即可获取到。

以下是构建所用到的表名
集合A --- `framework_dump_apis` framework可执行文件dump后的api集合
集合B --- `framework_header_apis` framework暴露的头文件api集合
集合C --- `document_apis` 内置文档docset数据集合
集合D --- `all_private_apis` 最终私有apis集合
集合E --- `private_framework_dump_apis` 私有framework可执行文件dump后的集合
集合F --- `framework_private_apis` 集合A - 集合B - 集合 C剩下的apis
集合G --- `white_list_apis` 白名单


#### TODO
1、class-dump有些文件会报错，需要查看下
2、mach-o文件中的依赖除了系统，是不是还需要dump第三方其他的库进行扫描`@xpath`
3. 私有api在公开的Framework及私有的PrivateFramework都有。
4. 请暂时暂mac上运行，linux上暂时没有找到合适的、代替otool的工具
5.9.2.5的iOS系统对应的Xcode 8是有docset的，后面的Xcode都有新的文件格式了，博客有介绍，需要自己分析，但是有点乱
TODO: 慢慢完善，写个博客记录下



