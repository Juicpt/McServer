# -*- coding: utf-8 -*-
# @Time    : 18-1-2 下午10:23
# @Author  : Juicpt
# @Site    : 
# @File    : consumers.py
# @Software: PyCharm

import json,psutil,platform
from channels.generic.websockets import WebsocketConsumer

# 实时获取CPU,内存信息
class MyConsumer(WebsocketConsumer):
    strict_ordering = False

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





