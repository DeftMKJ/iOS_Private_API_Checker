import re


def get_apis_from_header_file(filepath):
    with open(filepath) as f:
        text = f.read()
        apis = extract(text)
        return apis
    return []

"""
1.读入内存，取出头文件文本内容
2.过滤注释 // /**/
3.过滤@protocol xxx, xxx; 这种特殊字符串
4.取出@interface和@protocol两块内容
5.匹配带参或者不带参的Method ClassName，Type，组成{}返回
6.删除interface和protocol两大块
7.匹配c方法 {'type': 'C/C++', 'ctype': ['Coretext']}
"""
def extract(text):
    no_comment_text = remove_comment(text)
    method = []
    method += get_objc_func(no_comment_text)
    no_class = remove_objc(no_comment_text)
    method += get_c_func(no_class)
    return method


# 移除注释 // MULTILINE 模式  /* */ DOTALL模式
def remove_comment(text):
    def handler(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, handler, text)


def get_objc_func(text):
    """
    获取objc的方法
    :param no_comment_text 移除评论的文本:
    :return: [{"":"","":"","":""}]
    """

    def _get_methods(text):
        """
        有参数
        + (void)_performExpiringActivityWithReason:(id)arg1 usingBlock:(CDUnknownBlockType)arg2;
        ['_performExpiringActivityWithReason:', 'usingBlock:']

        无参数
        + (void)_expireAllActivies;
        []

        ['_performExpiringActivityWithReason:usingBlock:',
         '_performActivityWithOptions:reason:usingBlock:',
         '_expireAllActivies',
         '_dumpExpiringActivitives',
         '_expiringActivities',
         '_expirationHandlerExecutionQueue',
         '_expiringTaskExecutionQueue',
         '_expiringAssertionManagementQueue',
         '_fireExpirationHandler',
         '_reactivate',
         '_end',
         'debugDescription',
         'dealloc',
         '_initWithActivityOptions:reason:expirationHandler:']
        :param text:
        :return: # 文件扫描结束后方法列表
        """

        # 有参数方法
        method = re.compile("([+-] \([ *\w]*\).*?;)\s*")
        # 去参数 提取方法
        method_args = re.compile("(\w+:)")

        # 无参数方法提取  ?!的例子如下
        #  a = re.compile(r'windows(?!7|8|9|10|xp)')
        #  x = a.match('windows10') 后缀除了上面几个，才会匹配到windows，而且不会作为值进行group捕获
        method_no_args = re.compile("[+-] \([\w *]+\)\s*(\w+)(?!:)")
        temp = []
        for m in method.finditer(text):
            if m:
                mline = m.groups()[0]
                args = re.findall(method_args, mline)
                if len(args) > 0:
                    temp.append("".join(args))
                else:
                    no_args = method_no_args.search(mline)
                    if no_args:
                        temp.append(no_args.groups()[0])

        return temp

    # 移除@protocol NSObject, OS_voucher;这种格式，避免后面的interface和protocol获取域不对
    remove_pro = re.compile("@protocol [\w ,]*;", )
    text = re.sub(remove_pro, "", text)

    # interface 域
    interface = r"""
            @interface\s*
            .*?
            @end
        """
    # protocol 域
    protocol = r"""
            @protocol\s*
            .*?
            @end
        """
    # 获取classname正则
    class_name = re.compile("@interface\s*([\s\(\)\w]*)")
    # 获取interface正则编译
    inter_reg = re.compile(interface, re.VERBOSE | re.MULTILINE | re.DOTALL)
    methods = []
    # finditer查找匹配迭代器 匹配到一组或者多组@interface @end
    classes = [m.group(0) for m in inter_reg.finditer(text) if m.group(0)]
    for c in classes:
        # 搜索到类名
        cm = class_name.search(c)
        if cm:
            # 类名trim
            cn = cm.groups()[0].replace(" ", "")
            cn = cn.strip()
        # 获取方法
        temp = _get_methods(c)
        if temp:
            methods.append({"class": cn, "methods": temp, "type": "interface"})

    protocol_reg = re.compile(protocol, re.VERBOSE | re.MULTILINE | re.DOTALL)
    protocols = [m.group(0) for m in protocol_reg.finditer(text) if m.group(0)]
    # 协议方法 @protocol OS_dispatch_queue;
    valid_protocol = re.compile("@protocol\s*[\w, ]*;")
    # 协议名 @protocol NSDecimalNumberBehaviors
    protocol_name = re.compile("@protocol\s*(\w*)")
    for p in protocols:
        valid = valid_protocol.search(p)
        if valid:
            # 这种是要移除的 最上面已经做了移除
            continue
        else:
            pm = protocol_name.search(p)
            if pm:
                pn = pm.groups()[0].replace(" ", "")
                pn = pn.strip()
            temp = _get_methods(p)
            if temp:
                methods.append({"class": pn, "methods": temp, "type": "protocol"})
    return methods


def remove_objc(text):
    """
    移除interface和protocol
    :param text:
    :return:
    """
    p = r"""
            @interface\s*
            .*?
            @end
            |
            @protocol\s*
            .*?
            @end
    """
    pattern = re.compile(p, re.VERBOSE | re.MULTILINE | re.DOTALL)
    return re.sub(pattern, "", text)


def get_c_func(text):
    """
    获取c方法
    :param text:
    :return:[{'type': 'C/C++', 'ctype': ['Coretext']}]
    """
    # delete struct and enum declariations
    del_struct_enum = r"""
        (?:typedef)?\s*struct\s*\w+\s*{[^}]*}\s*\w*;   # struct
        |
        \s*enum\s*{[^}]*\s*};  # enum
        |
        \s*{[^{}]*\s*}     #  function implement
    """
    del_regex = re.compile(del_struct_enum, re.VERBOSE|re.MULTILINE|re.DOTALL)
    text = re.sub(del_regex, "", text)
    pattern = r"""
        #^(?!\#)(?!\s*typedef\s\w+).*?(\w+)\s*\((?!\w+,)(?![^()*^]*(?:\d+_\d+|NA))
        ^(?!\#)(?!\s*typedef\s\w+).*?(\w+)\s*\((?!\w+,)(?!\d+_\d+|NA,)
        |
        \([*^]([^)]+)\)\s*\(
        |
        \#define\s*(\w+)\s?\(\s*\w*
    """
    #regex = re.compile(pattern)
    regex = re.compile(pattern, re.VERBOSE|re.MULTILINE)
    #regex = re.compile(pattern, re.VERBOSE|re.MULTILINE|re.DOTALL)
    #regex = re.compile(pattern, re.MULTILINE)
    #method = [m.group(1) for m in regex.finditer(text) if m.group(1)]
    #method = [m.group(0) for m in regex.finditer(text) if m.group(0)]
    #method = re.findall(regex, text)
    method = []
    for mm in regex.finditer(text):
        m = mm.groups()
        if m[0]:
            method.append(m[0])
        elif m[1]:
            method.append(m[1])
        elif m[2]:
            method.append(m[2])
    s = set(method)
    method = list(s)
    if len(method) > 0:
        return [{"class":"ctype", "methods":method, "type":"C/C++"}]
    else:
        return []


if __name__ == '__main__':
    class_info = get_apis_from_header_file('/Users/mikejing191/PASmartpay/Library/gmssl/openssl/aes.h')
    print(class_info)