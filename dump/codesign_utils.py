import subprocess
import re



def codesignapp(app_path):
    cmd = 'codesign -vv -d %s '%app_path
    results =  subprocess.getstatusoutput(cmd)

    if results and len(results) == 2 and results[0] == 0:
        results = results[1]
        codesigin = re.compile(r'Authority=(.*)', re.MULTILINE | re.VERBOSE)
        x = codesigin.findall(results)
        if x and len(x) > 2:
            results = x[0] + ' / ' + x[1]
        else:
            results = ''
    else:
        results = ''
    return results

if __name__ == '__main__':
    res = codesignapp('/Users/mikejing191/Desktop/SmartPay_Example-IPA/Payload/SmartPay_Example.app/SmartPay_Example')
    print(res)
    # codesigin = re.compile(r'Authority=(.*)', re.MULTILINE | re.VERBOSE)
    # x =  codesigin.findall(res)
    # print('*'*10)
    # print(x)



