import re


def fun(m):
    return m.group().upper()


pattern = re.compile(r'like', re.I)

s1 = pattern.sub(fun, "I like you, do you like me?")
print(s1)


def remove_comments(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


x = '//\n//  ""   Generated by class-dump 3.5 (64 bit) (Debug version compiled May 29 2019 15:54:17).\n//\n//  Copyright (C) 1997-2019 Steve Nygard.\n//\n\n#import <Foundation/NSSingleByteEncodingDetector.h>\n\n__attribute__((visibility("hidden")))\n@interface NSWINDOWS1252EncodingDetector : NSSingleByteEncodingDetector\n{\n}\n\n/*的代课老师\n 狂蜂浪蝶\n dsdsdsdsds\n */\n- (unsigned long long)recognizeString:(const char *)arg1 withDataLength:(unsigned long long)arg2 intoBuffer:(id)arg3;\n\n@end\n\n\n'

y = '//\n//     Generated by class-dump 3.5 (64 bit) (Debug version compiled May 29 2019 15:54:17).\n//\n//  Copyright (C) 1997-2019 Steve Nygard.\n//\n\n@class NSCoder;\n\n@protocol NSCoding\n- (id)initWithCoder:(NSCoder *)arg1;\n- (void)encodeWithCoder:(NSCoder *)arg1;\n@end\n\n'

z = '//\n//     Generated by class-dump 3.5 (64 bit) (Debug version compiled May 29 2019 15:54:17).\n//\n//  Copyright (C) 1997-2019 Steve Nygard.\n//\n\n#import <objc/NSObject.h>\n\n@class BKSProcessAssertion, NSString;\n@protocol NSObject, OS_voucher;\n\n__attribute__((visibility("hidden")))\n@interface _NSActivityAssertion : NSObject\n{\n    unsigned long long _options;\n    NSString *_reason;\n    unsigned int _systemSleepAssertionID;\n    NSObject<OS_voucher> *_voucher;\n    NSObject<OS_voucher> *_previousVoucher;\n    unsigned char _adoptPreviousVoucher;\n    id <NSObject> _xpcBoost;\n    BKSProcessAssertion *_processAssertion;\n    CDUnknownBlockType _expirationHandler;\n    struct os_unfair_lock_s _lock;\n    _Atomic _Bool _ended;\n}\n\n+ (void)_performExpiringActivityWithReason:(id)arg1 usingBlock:(CDUnknownBlockType)arg2;\n+ (void)_performActivityWithOptions:(unsigned long long)arg1 reason:(id)arg2 usingBlock:(CDUnknownBlockType)arg3;\n+ (void)_expireAllActivies;\n+ (void)_dumpExpiringActivitives;\n+ (id)_expiringActivities;\n+ (id)_expirationHandlerExecutionQueue;\n+ (id)_expiringTaskExecutionQueue;\n+ (id)_expiringAssertionManagementQueue;\n- (void)_fireExpirationHandler;\n- (void)_reactivate;\n- (void)_end;\n- (id)debugDescription;\n- (void)dealloc;\n- (id)_initWithActivityOptions:(unsigned long long)arg1 reason:(id)arg2 expirationHandler:(CDUnknownBlockType)arg3;\n\n@end\n\n'

# p = remove_comments(x)
# print(p)

def replacer1(match):
    s = match.group(0)
    if s.startswith('/'):
        return "wocao111"
    else:
        return s


a = '// 3232\n\n//\n //dsdsdsdsd'
b = '/*\n\nxsdsdsfdfdfd*/'
c = '//\n//     Generated by class-dump 3.5 (64 bit) (Debug version compiled May 29 2019 15:54:17).\n//\n//  Copyright '
pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.MULTILINE | re.DOTALL)
no_comment = re.sub(pattern, replacer1, z)
print(no_comment)

result = re.sub(re.compile("(@protocol|@class) [\w ,]*;", ), "", no_comment)
print(result)

# class_reg = re.compile("@interface\s*([\s\(\)\w]*)")
# ppp = re.findall(class_reg, result)
# print(ppp)


interface = r"""
        @interface\s*
        .*?
        @end
    """
# inter_reg = re.compile(interface, re.DOTALL | re.MULTILINE | re.VERBOSE)
# print(re.findall(inter_reg, result))

# d = 'abbbb'
# print(re.match(r'ab*?', d).group())

# DOTALL 模式
# \*
# 主要
# 针对
# 这蔗农
# *\

# MULTILINE 多行匹配模式


#
# p1 = re.compile(r'"(?:\\.|[^\\"])*"')
# print(p1.sub('mkj','"dsdsds"'))
print("*" * 50)

class_name = re.compile("@interface\s*([\s\(\)\w]*)")
inter_reg = re.compile(interface, re.VERBOSE | re.MULTILINE | re.DOTALL)
methods = []
classes = [m.group(0) for m in inter_reg.finditer(result) if m.group(0)]
for c in classes:
    # print(c)
    cls = class_name.search(c)
    print(cls.groups())

print()

def _get_methods(text):
    method = re.compile("([+-] \([ *\w]*\).*?;)\s*")
    # method_args = re.compile("(\w+:)\([\w *^()]*\)\w+ ?")
    method_args = re.compile("(\w+:)")
    # method_no_args = re.compile("[+-] \(.*?\)(\w*)(?:\s*\S*);")
    # method_no_args = re.compile("[+-] \([\w *]+\)\s*(\w*)\s*")
    method_no_args = re.compile("[+-] \([\w *]+\)\s*(\w+)(?!:)")
    temp = []
    for m in method.finditer(text):
        if m:
            # temp.append(m.groups()[0])
            mline = m.groups()[0]
            print(mline)
            args = re.findall(method_args, mline)
            print(args)
            if len(args) > 0:
                temp.append("".join(args))
            else:
                no_args = method_no_args.search(mline)
                if no_args:
                    temp.append(no_args.groups()[0])
    print(temp)
    return temp


_get_methods(result)