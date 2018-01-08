from django.shortcuts import render,reverse
from django.views.generic.base import View
from django.http import HttpResponse,JsonResponse,HttpResponseNotFound,QueryDict
import json,paramiko,urllib,MC,sys,os,random,string,time
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import server,ip_or_api,add_way,mc_inf
from connect import con_client


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class profile(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self,request,id):


        table={
            'generator-settings':'用于自定义超平坦世界的生成，不生成超平坦世界请留空',
            'allow-nether':'是否允许下界（包括地狱）',
            'level-name':'世界（地图）名称 不要使用中文',
            'enable-query':'是否允许使用GameSpy4协议的服务器监听器',
            'allow-flight':'是否允许玩家飞行（在任何游戏模式下）',
            'server-port':'服务器端口',
            'level-type':'地图的生成类型',
            'enable-rcon':'是否允许远程访问服务器控制台',
            'force-gamemode':'强制玩家加入时为默认游戏模式',
            'level-seed':'地图种子 默认留空',
            'server-ip':'服务器ip，若不绑定请留空',
            'max-build-height':'玩家在服务器放置方块的最高高度',
            'spawn-npcs':'是否生成村民',
            'white-list':'是否开启白名单',
            'spawn-animals':'是否生成动物',
            'snooper-enabled':'启用数据采集',
            'hardcore':'极限模式（死后自动封禁）',
            'texture-pack':'材质包',
            'online-mode':'在线（正版）验证',
            'pvp':'是否允许玩家掐架',
            'difficulty':'难度0=和平 1=简单 2=普通 3=困难',
            'player-idle-timeout':'允许的挂机时间，单位为分钟 超过限制后自动T出服务器',
            'gamemode':'游戏模式 0=生存 1=创造 2=冒险 3=旁观',
            'max-players': '服务器最大玩家数限制',
            'spawn-monsters':'生成攻击型生物（怪物）',
            'view-distance': '服务器发送给客户端的数据量，决定玩家能设置的视野',
            'generate-structures': '生成世界时生成结构（如村庄）禁止后地牢和地下要塞仍然生成',
            'motd': '服务器信息展示 若使用ColorMotd等插件可留空该选项',
            'op-permission-level': 'OP权限等级',
            'announce-player-achievements': '玩家获得成就时，是否在服务器聊天栏显示（是否允许其装X）',
            'network-compression-threshold': '网络压缩阈值',
            'resource-pack-sha1': '资源包的SHA-1值，必须为小写十六进制，不是必填选项',
            'enable-command-block': '启用命令方块',
            'resource-pack': '统一资源标识符 (URI) 指向一个资源包。玩家可选择是否使用',
            'max-world-size': '最大世界大小',
            'prevent-proxy-connections':'',
            'use-native-transport':'',
            'max-tick-time':'',


        }


        return render(request,'profile.html',{'table':table})

    def post(self,request,id):
        server_id = mc_inf.objects.get(id=id).server.id
        name = mc_inf.objects.get(id=id).name
        ip = server.objects.get(id=server_id).ip
        secrect = server.objects.get(id=server_id).secrect.encode('utf-8')
        if request.POST.get('data') == 'data':
            try:
                connect = con_client(ip, secrect)
            except ConnectionRefusedError:

                return JsonResponse({'erro':'erro'})
            data = {'type':'cmd','step':'process','control':'profile','cmd':'get','name':name}
            data = json.dumps(data)
            connect.send(data)
            getdata = connect.recv()
            connect.close()
            get_data = json.loads(getdata)

            return JsonResponse(get_data)
        else:
            try:
                connect = con_client(ip, secrect)
            except ConnectionRefusedError:
                return JsonResponse({'erro':'erro'})
            for key,value in request.POST.items():
                data = {'type': 'cmd', 'step': 'process', 'control': 'profile', 'cmd': 'save', 'name': name,'key':key,'value':value}
                data = json.dumps(data)
                connect.send(data)
                getdata = connect.recv()


            connect.close()
            return JsonResponse({'ok':'ok'})



class game(LoginRequiredMixin,View):

    login_url = '/login/'

    def get(self,request):
        user = request.user
        ip = server.objects.filter(user_id = user.id)
        a= user.server_set.all()
        value={}
        for x in a:
            value[x.ip] = {}
            for y in x.mc_inf_set.all():
                value[x.ip][y.name] = y.id
        return render(request,'server.html',{'msg':value,'ip':ip})
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
            return render(request, 'game.html',{'name':name,'id':id})


# 游戏启动重启关闭
class game_inf(LoginRequiredMixin,View):
    login_url = '/login/'
    def post(self,request):
        control= request.POST.get('control')
        id = request.POST.get('id')
        name = mc_inf.objects.get(id=id).name
        try:
            secrect = mc_inf.objects.get(id=id).server.secrect.encode('utf-8')
            connect = con_client(mc_inf.objects.get(id=id).server.ip,secrect)
        except ConnectionRefusedError:
            return JsonResponse({'java_version': '连接不上服务器'})
        data={'type':'cmd','step':'process','control':control,'name':name,'mc':'server'}
        data = json.dumps(data)
        connect.send(data)
        inf = connect.recv()
        connect.close()
        return JsonResponse({'ok':'ok'})





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
            connect.close()
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
            connect.close()
            return JsonResponse({'ok': inf})
        else:
            print('参数错误')
            return HttpResponse('参数错误')




