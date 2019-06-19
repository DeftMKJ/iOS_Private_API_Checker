import sys
import subprocess

# with open('/Users/mikejing191/Desktop/111.txt','rb') as f:
#     text = f.read()
#     print(text.decode('utf-8'))

if __name__ == '__main__':
    path = '/Users/mikejing191/Desktop/T2'
    cmd = u'python -mmacholib find %s'%path

    x =  subprocess.check_output(cmd.split())
    print(x)
    for path in x.split():
        print(path.decode('utf-8'))
