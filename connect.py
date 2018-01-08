#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket,json

import hmac
import os

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




