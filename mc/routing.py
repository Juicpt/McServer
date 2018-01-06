# -*- coding: utf-8 -*-
# @Time    : 18-1-2 下午10:24
# @Author  : Juicpt
# @Site    : 
# @File    : routing.py
# @Software: PyCharm


from channels.routing import route
from websocket.consumers import MyConsumer

channel_routing = [
    MyConsumer.as_route(path=r"^/chat/"),
]