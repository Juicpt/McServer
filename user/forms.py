# -*- coding: utf-8 -*-
# @Time    : 18-1-2 下午10:31
# @Author  : Juicpt
# @Site    : 
# @File    : form.py
# @Software: PyCharm


from django import forms

class LoginForm(forms.Form):
    userid = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=2)