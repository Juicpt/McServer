#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading
import time
import subprocess
import random
import os
import re
import json
import hmac
import sys
import tempfile
# 服务器命令执行
class cmd(object):

    def __init__(self,cwd):
        self.server = None
        self.tmpFile = '/tmp/%s.tmp' % random.randint(10000, 999999)
        self.cwd = cwd
    # 命令执行
    def start(self,cmd):
        with open(self.tmpFile, 'w') as fpWrite:
            self.server = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=fpWrite, stderr=subprocess.STDOUT,cwd=self.cwd,shell=True)
    # 服务器命令传递
    def run_cmd(self,command):
        if command != 'stop':
            self.server.stdin.write(bytes(command + "\r\n", "ascii"))
            self.server.stdin.flush()
        else:
            self.server.stdin.write(bytes(command + "\r\n", "ascii"))
            self.server.stdin.flush()
            os.popen('rm -rf %s' % self.tmpFile)

    # 日志获取
    def read_log(self,sock):
        with open(self.tmpFile, 'r') as file:
            while True:
                where = file.tell()
                line = file.readline()
                if not line:
                    time.sleep(1)
                    file.seek(where)
                else:
                    sock.send(line.encode('utf-8'))


class properties(object):
    def __init__(self,name):

        self.file_name = '/home/' + name + '/server.properties'
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


class connection(object):

    def __init__(self,secret_key):
        # 声明动态变量,用于进程管理
        self.a = locals()
        self.secret_key = secret_key.encode('utf-8')
    # 通讯认证
    def client_authenticate(self,connection, secret_key):
        message = os.urandom(32)
        connection.send(message)
        hash = hmac.new(secret_key, message)
        digest = hash.digest()
        response = connection.recv(len(digest))
        return hmac.compare_digest(digest, response)
    # 认证过后消息传递
    def echo_handler(self,client_sock,address):
        if not self.client_authenticate(client_sock, self.secret_key):
            client_sock.close()
            return

        while True:
            msg = client_sock.recv(1024).decode('utf-8')
            if not msg:
                break
            t = threading.Thread(target=self.tcplink, args=(client_sock,address,msg))
            t.start()

        client_sock.close()
        print('Connection from %s:%s closed.' % address)
    # 多线程连接
    def tcplink(self,sock,addr,data):
        print('Accept new connection from %s:%s...' % addr)
        data = json.loads(data)
        # 开服相关命令实现
        if data["type"] == 'cmd':

            if data['step'] == 'start':
                address = data['address']
                cwd = os.getcwd()+'/'+ data['name']
                subprocess.check_call('mkdir %s' %data['name'],shell=True,cwd = os.getcwd())
                subprocess.check_call('wget %s' %address,shell=True,cwd = cwd)
                subprocess.check_call('echo eula=true>eula.txt', shell=True, cwd=cwd)
                sock.send('ok'.encode('utf-8'))

            elif data['step'] == 'process':
                if data['control'] == 'start':
                    cwd = '/home/' + data['name']+'/'
                    ml = '/home/' + data['name']+'/' + data['mc']
                    self.a[data['name']] = cmd(cwd)
                    self.a[data['name']].start('java -jar %s' % ml)
                    sock.send('ok'.encode('utf-8'))

                elif data['control'] == 'stop':
                    self.a[data['name']].run_cmd('stop')
                    sock.send('ok'.encode('utf-8'))

                elif data['control'] =='restart':
                    cwd = '/home/' + data['name'] + '/'
                    ml = '/home/' + data['name'] + '/' + data['mc']
                    self.a[data['name']].run_cmd('stop')
                    self.a[data['name']] = cmd(cwd)
                    self.a[data['name']].start('java -jar %s' % ml)
                    sock.send('ok'.encode('utf-8'))

                elif data['control'] =='cmd':
                    self.a[data['name']].run_cmd(data['cmd'])
                    sock.send('ok'.encode('utf-8'))
                elif data['control'] =='profile':
                    name = data['name']
                    if data['cmd'] == 'get':
                        data = properties(name).get_dict()
                        data = json.dumps(data)
                        sock.send(data.encode('utf-8'))
                    elif data['cmd'] == 'save':
                        properties(name).put(data['key'],data['value'])
                        sock.send('ok'.encode('utf-8'))




            elif data['step'] == 'end':
                cwd = os.getcwd()
                name = data['name']
                subprocess.check_call('rm -rf %s' %name,shell=True,cwd= cwd)


        # 日志读取
        elif data["type"] == 'log':
            while True:
                try:
                    self.a[data["name"]].read_log(sock)
                except socket.error as msg:
                    print("连接中断",msg)
                    break
                finally:
                    sock.send('erro'.encode('utf-8'))
                    break
        # Java版本检查安装
        elif data["type"] == 'java':
            if data['control'] == 'check':
                sock.send(java().java_version())
            elif data['control'] == 'install':
                if data['java_version'] == '7':
                    java().java_install(7)
                    sock.send('ok'.encode('utf-8'))
                elif data['java_version'] == '8':
                    java().java_install(8)
                    sock.send('ok'.encode('utf-8'))
            else:
                sock.send('erro'.encode('utf-8'))


    # 连接监听
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', 9999))
        s.listen(5)
        print('Waiting for connection...')
        while True:
            sock, address = s.accept()
            self.echo_handler(sock,address)



class java(object):

    def java_install(self,n):
        openjdk_ppa = 'sudo add-apt-repository ppa:openjdk-r/ppa'
        java_ppa = 'sudo add-apt-repository ppa:webupd8team/java -y'
        update = 'sudo apt-get update'
        openjdk7 = 'sudo apt-get install -y openjdk-7-jdk'
        jdk7 = 'sudo apt-get install -y oracle-java7-installer'
        jdk8 = 'sudo apt-get install -y oracle-java8-installer'
        jdk7_acc = 'echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections'
        jdk8_acc = 'echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections'

        if n == 7:
            subprocess.check_call(openjdk_ppa, shell=True)
            subprocess.check_call(update, shell=True)
            subprocess.check_call(openjdk7, shell=True)
        elif n == 8:
            subprocess.check_call(java_ppa, shell=True)
            subprocess.check_call(update, shell=True)
            subprocess.check_call(jdk8_acc, shell=True)
            subprocess.check_call(jdk8, shell=True)
        else:
            print('erro')


    def java_version(self):
        try:
            version_inf = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
            pattern = '\"(\d+\.\d+).*\"'
            version = re.search(pattern, version_inf.decode('utf-8')).groups()[0].encode('utf-8')
            return version
        except FileNotFoundError:
            return 'None'.encode('utf-8')


if __name__ == '__main__':
    a = connection(sys.argv[1])
    a.start()
