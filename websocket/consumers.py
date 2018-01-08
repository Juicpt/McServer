# -*- coding: utf-8 -*-
# @Time    : 18-1-2 下午10:23
# @Author  : Juicpt
# @Site    : 
# @File    : consumers.py
# @Software: PyCharm

import json,psutil
from channels.generic.websockets import WebsocketConsumer,JsonWebsocketConsumer
from connect import con_client
from user.models import server,ip_or_api,add_way,mc_inf

# 实时获取CPU,内存信息
class MyConsumer(WebsocketConsumer):
    strict_ordering = False
    http_user_and_session = True

    def connection_groups(self, **kwargs):

        return['test']

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})

    def receive(self, text=None, bytes=None, **kwargs):
        cpu = psutil.cpu_percent(interval=0.1, percpu=False)
        mem = psutil.virtual_memory().percent
        self.send(text=json.dumps({
            "cpu": cpu,
            "mem": mem,
            "status": 1,
        }))

# 日志获取
class cmd(JsonWebsocketConsumer):
    strict_ordering = False
    http_user_and_session = True


    def connect(self, message, **kwargs):
        name = str(self.message.user)

        if name == 'AnonymousUser':
            message.reply_channel.send({"close": True})
        else:
            self.message.reply_channel.send({"accept": True})



    def receive(self, content, **kwargs):

        print(content)
        self.send({'ok':'ok'})


    def disconnect(self, message, **kwargs):
        print('连接断开')


