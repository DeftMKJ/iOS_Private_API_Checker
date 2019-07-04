import json
# /Applications/Xcode.app/Contents/SharedFrameworks/DNTDocumentationSupport.framework/Versions/A/Resources/external
# map.db和cache.db两个文件的定位到fs文件夹下对应的文件 lzfse -decode -i 1605 -o 1605.decoded.json
# 压缩算法实现 https://github.com/lzfse/lzfse


# instm 对象方法 instance method
# func  C方法
# clm 类方法
# intfm 协议对象方法 interface method
# intfcm 协议类方法 interface class method
# instp  backgroundColor Category属性 instance property





def get_decode_json(filepath):
    with open(filepath, 'rb') as f:
        text = f.read()
        filter_text = text.decode('utf-8', 'ignore')
        # print(filter_text)
        return filter_text
    return []
# 2439 是UIView
if __name__ == '__main__':
    result = get_decode_json('/Users/mikejing191/Desktop/2035.decode.json')

    num = 0
    result_array = result.split('}{')

    result = ''

    for str in result_array:
        print('')
        if num == 0:
            js = str + '}'
        elif num == len(result_array)-1:
            js = '{' + str
        else:
            js = '{' + str + '}'
        num += 1
        print(js)

    print(type(result))
    print(result)
    a = "{'a' : '1'}"


    b = eval(a)
    print(b)

    x = eval(result)
    print(x)

    # x =  json.dumps(result)
    # print(x)
    # b = eval(result)
    # print(b)


