from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm
from django.http import HttpResponse,HttpResponsePermanentRedirect
from django.urls import reverse
import psutil,json,platform,paramiko,urllib
from django.contrib.auth.mixins import LoginRequiredMixin

# 登录
class LoginView(View):

    def get(self,request):
        return render(request,"login.html",{})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("userid","")
            pass_word = request.POST.get("password","")
            user = authenticate(username = user_name,password = pass_word)
            if user is not None:
                login(request,user)
                return HttpResponsePermanentRedirect(reverse('index'))
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误'})
        else:
            return render(request,'login.html',{'login_form':login_form})

# 登出
class LogoutView(View):


    def get(self,request):
        logout(request)

        return HttpResponsePermanentRedirect(reverse('login'))



# 首页服务器基本信息获取
class HomeView(LoginRequiredMixin,View):

    login_url = '/login/'

    def get(self,request):
        py_version = platform.python_version()
        sys = platform.uname()
        ip = urllib.request.urlopen('https://api.ip.sb/ip').read().decode('utf-8')
        cpu = platform.processor()
        mem = str(psutil.virtual_memory().total/(1024*1024)) + "Mb"
        return render(request,'index.html',{'py_version':py_version,'sys':sys,'ip':ip,'cpu':cpu,'mem':mem})


