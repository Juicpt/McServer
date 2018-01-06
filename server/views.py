from django.shortcuts import render,reverse
from django.views.generic.base import View
from django.http import HttpResponse,JsonResponse,HttpResponseNotFound
import json,paramiko,urllib,MC,sys,os,random,string,time
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import server,ip_or_api,add_way,mc_inf
from connect import con_client


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class game(LoginRequiredMixin,View):

    login_url = '/login/'

    def get(self,request):
        user = request.user
        a= user.server_set.all()
        value={}
        for x in a:
            value[x.ip] = {}
            for y in x.mc_inf_set.all():
                value[x.ip][y.name] = y.id
        return render(request,'server.html',{'msg':value})
    # 信息提交
    def post(self,request):
        name = request.POST.get('name')
        ip = request.POST.get('ip')
        version = request.POST.get('version')
        server_id = server.objects.get(ip=ip)

        game = mc_inf(name=name,server=server_id)
        try:
            secrect = server.objects.get(ip=ip).secrect.encode('utf-8')
            connect = con_client(ip, secrect)
        except ConnectionRefusedError:
            id = server.objects.get(ip=ip).id
            return JsonResponse({'java_version': '连接不上服务器', 'id': id})
        address = 'https://bmclapi2.bangbang93.com/version/%s/server' %version
        data = {'type':'cmd','step':'start','address':address,'name':name}
        data = json.dumps(data)
        connect.send(data)
        if connect.recv() =='ok':
            game.save()
        return JsonResponse({'ok':'ok'})


class add_game(LoginRequiredMixin,View):

    login_url = '/login/'

    def get(self,request,id):
        user_id = mc_inf.objects.get(id=id).server.user.id
        name = mc_inf.objects.get(id=id).name
        if  user_id== request.user.id:
            return render(request, 'game.html',{'name':name})







class setting(LoginRequiredMixin,View):

    login_url = '/login/'

    def get(self,request):
        ip = server.objects.all()


        return render(request,'setting.html',{'ip':ip})
    # 服务器信息提交
    def post(self,request):
        add_type = request.POST.get('add_type')
        if add_type == 'ip':
            ip = request.POST.get('ip')
            user = request.POST.get('user')
            pw = request.POST.get('password')
            try:
                # 传输客户端文件
                t = paramiko.Transport((ip,22))
                t.connect(username= user, password = pw)
                sftp = paramiko.SFTPClient.from_transport(t)
                remotepath = '/home/'
                localpath = BASE_DIR + '/static/client/'
                file = os.listdir(BASE_DIR + '/static/client/')
                for f in file:
                    sftp.put(os.path.join(localpath,f), os.path.join(remotepath,f))
                t.close()

                # 密钥生成
                secrect = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                server_inf = server(ip=ip, secrect=secrect,user_id=request.user.id)
                # 执行客户端进程
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=ip, port=22, username=user, password=pw)
                transport = client.get_transport()
                channel = transport.open_session()
                channel.exec_command('sudo apt-get update && sudo apt-get install screen -y && python3 /home/client.py '+secrect+' >/dev/null 2>&1 &')
                client.close()
                channel.close()
                server_inf.save()
                time.sleep(1)
                ip = ip_or_api(server = server.objects.get(ip = ip),add_way = add_way.objects.get(name='ip'))
                ip.save()

                return HttpResponse('ok')
            except BaseException as a :

                return HttpResponse(str(a))

            except AuthenticationException:
                return HttpResponse('验证失败')

        elif add_type == 'api':
            return HttpResponse('api')

        else:
            return HttpResponse('错误提交')



class java(View):

    def get(self,request):
        return HttpResponse('ok')

    def post(self,request):
        check = request.POST.get('cmd')
        if check == 'check':
            ip = request.POST.get('ip')
            try:
                secrect = server.objects.get(ip=ip).secrect.encode('utf-8')
                connect = con_client(ip, secrect)

            except ConnectionRefusedError:
                id = server.objects.get(ip=ip).id
                return JsonResponse({'java_version':'连接不上服务器','id':id})

            data ={'type':'java','control':'check'}
            data = json.dumps(data)
            connect.send(data)
            version = connect.recv()
            if version == 'None':
                id = server.objects.get(ip=ip).id
                return JsonResponse({'java_version': version,'id':id})
            else:
                id = server.objects.get(ip=ip).id
                a = server.objects.get(ip=ip)
                a.java =True
                a.java_version = version
                a.save()

                return JsonResponse({'java_version': version, 'id': id})

        elif check == 'install':
            java = request.POST.get('java')
            ip = request.POST.get('ip')
            try:
                secrect = server.objects.get(ip=ip).secrect.encode('utf-8')
                connect = con_client(ip, secrect)
            except ConnectionRefusedError:
                return JsonResponse({'java_version':'连接不上服务器'})

            data = {'type':'java','control':'install','java_version':java}
            data = json.dumps(data)
            connect.send(data)
            inf = connect.recv()
            return JsonResponse({'ok': inf})
        else:
            print('参数错误')
            return HttpResponse('参数错误')




