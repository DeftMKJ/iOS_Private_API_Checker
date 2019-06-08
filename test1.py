import sys

with open('/Users/mikejing191/Desktop/111.txt','rb') as f:
    text = f.read()
    print(text.decode('utf-8'))