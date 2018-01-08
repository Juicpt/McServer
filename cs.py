# -*- coding: utf-8 -*-
# @Time    : 17-12-7 下午7:56
# @Author  : Juicpt
# @Site    : 
# @File    : cs.py
# @Software: PyCharm

import re
import tempfile
import os

class properties(object):
    def __init__(self):
        self.file_name = '/home/juicpt/server/server.properties'
        self.properties = {}
        try:
            with open(self.file_name, 'r') as fpwrite:
                for line in fpwrite:
                    if line.find('=') > 0 and not line.startswith('#'):
                        key=line.replace('\n', '').split('=')
                        self.properties[key[0]]=key[1]

        except Exception as e:
            print(e)

    def get_dict(self):
        return self.properties

    def put(self,key,value):
        self.properties[key] = value
        self.replace_property(key + '=.*' , key + '=' + value,True)

    def replace_property(self,from_regex,to_str,append_on_not_exists = True):
        file = tempfile.TemporaryFile(mode='w+t')
        if os.path.exists(self.file_name):
            r_open = open(self.file_name,'r')
            pattern = re.compile('' + from_regex)
            found = None
            for line in r_open:
                if pattern.search(line) and not line.strip().startswith('#'):
                    found = True
                    line = re.sub(from_regex,to_str,line)
                file.write(line)

            if not found and append_on_not_exists:
                file.write('\n' + to_str)

            r_open.close()

            file.seek(0)

            content = file.read()

            if os.path.exists(self.file_name):
                os.remove(self.file_name)

            w_open =open(self.file_name,'w')
            w_open.write(content)
            w_open.close()


            file.close()

        else:
            print("file %s not fount" %self.file_name)





if __name__ == '__main__':

    properties().put('online-mode','false')

    for key,value in properties().get_dict().items():
        print(key,value)

    print(properties().get_dict())

