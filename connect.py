#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket,json

import hmac
import os

# def client_authenticate(connection, secret_key):
#     '''
#     Authenticate client to a remote service.
#     connection represents a network connection.
#     secret_key is a key known only to both client/server.
#     '''
#     message = connection.recv(32)
#     hash = hmac.new(secret_key, message)
#     digest = hash.digest()
#     connection.send(digest)
#
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 建立连接:
# s.connect(('192.161.51.161', 9999))
# # 接收欢迎消息:
# secret_key = b'9O1eBMZ3'
#
# client_authenticate(s,secret_key)
# data = json.dumps({"type":"log","cmd":['java','-jar','minecraft_server.1.12.2.jar'],"name":"c"}).encode('utf-8')
# s.send(data)
# while True:
#     print(s.recv(1024).decode('utf-8'))
#
# s.close()



class con_client(object):

    def __init__(self,ip,secret):
        self.secret_key = secret
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = self.s.connect((ip,9999))
        # 消息认证
        message = self.s.recv(32)
        hash = hmac.new(self.secret_key,message)
        digest = hash.digest()
        self.s.send(digest)
    def send(self,data):
        self.s.send(data.encode('utf-8'))

    def recv(self):
        data = self.s.recv(1024).decode('utf-8')
        return data

    def close(self):
        self.s.close()




