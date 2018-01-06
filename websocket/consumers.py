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
    # http_user = True
    # channel_session_user = True

    def connection_groups(self, **kwargs):

        return['test']

    def connect(self, message, **kwargs):
        self.message.reply_channel.send({"accept": True})
        print("链接状态")

    def receive(self, text=None, bytes=None, **kwargs):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        # Simple echo
        cpu = psutil.cpu_percent(interval=0.1, percpu=False)
        mem = psutil.virtual_memory().percent
        self.send(text=json.dumps({
            "cpu": cpu,
            "mem": mem,
            "status": 1,
        }))

    def disconnect(self, message, **kwargs):

        print("链接断开")

