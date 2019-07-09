import os
from pprint import pprint
def get_apis_from_header_file(filepath):
    with open(filepath, 'rb') as f:
        text = f.read()
        filter_text = text.decode('utf-8')
        # print(filter_text)
        # print('头文件读入，正在处理正则---> ' + filepath)
        print(filter_text)
    return []


if __name__ == '__main__':
    print("宓珂")
    # headers = '/Users/mikejing191/Desktop/iOS_Private_API_Checker/tmp/public_headers'

    # for f in os.listdir(headers):
    #     for x in os.listdir(os.path.join(os.path.join(headers,f), 'Headers')):
    #         get_apis_from_header_file(os.path.join(os.path.join(os.path.join(headers,f), 'Headers'), x))