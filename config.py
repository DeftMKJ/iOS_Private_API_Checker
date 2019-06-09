import os

sqlite3_info = {
    'sqlite3': 'mkj_private_apis.db'
}

class_dump_z_path = {
    'iphone': os.path.join(os.getcwd(), 'class_dump_z/iphone_armv6/class-dump-z'),
    'mac': os.path.join(os.getcwd(), 'class_dump_z/mac_x86/class-dump-z'),
    'linux': os.path.join(os.getcwd(), 'class_dump_z/linux_x86/class-dump-z'),
    'win': os.path.join(os.getcwd(), 'class_dump_z/win_x86/class-dump-z'),
}

sdks_configs = [
    {
        'sdk_version': '12.1',
        'framework_path': '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/CoreSimulator/Profiles/Runtimes/iOS.simruntime/Contents/Resources/RuntimeRoot/System/Library/Frameworks',
        # 'framework_header_path': '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator12.1.sdk/System/Library/Frameworks/',
        'framework_header_path': '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks',
        'private_framework_path': '/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/CoreSimulator/Profiles/Runtimes/iOS.simruntime/Contents/Resources/RuntimeRoot/System/Library/PrivateFrameworks',
        'docset_path': '/Users/mikejing191/Desktop/私有API学习/com.apple.adc.documentation.iOS.docset/Contents/Resources/docSet.dsidx.db',
    },
]

db_names = {
    "SET_A": "framework_dump_apis",  # 从公共的framework dump出来的所有API 包括有文档，头文件，没有文档还包括一些私有api
    "SET_B": "framework_header_apis",  # 从公共的framework 的header文件中解析出来的api
    "SET_C": "document_apis",  # 文档集合中解析出来的apis
    "SET_D": "all_private_apis",  # 所有API集合 F = (A - B - C)  F + E
    "SET_E": "private_framework_dump_apis",  # 从私有framework dump出来的所有apis
    "SET_F": "framework_private_apis",  # 从framework_dump_apis公有api中筛选出对应的私有API F = (A - B - C)
    "SET_G": "white_list_apis",  # 白名单

    # "SET_D": "except_document_apis",  # 除了文档之外的apis   sql2 - sql3
}
