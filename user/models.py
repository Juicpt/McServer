from django.db import models
from django.conf import settings


class cloud_api(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete='PROTECT')
    # name = models.CharField
    api_id  = models.CharField(blank=False,max_length=100,verbose_name='API_ID')
    api_secrect = models.CharField(blank=False,max_length=100,verbose_name='API_SECRECT')


    class Meta:
        db_table = 'api'
        verbose_name = 'API信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.api_id


class add_way(models.Model):
    name = models.CharField(max_length=100,verbose_name='添加方式名称')

    class Meta:
        db_table = 'add_way'
        verbose_name = '添加方式类型'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class ip_or_api(models.Model):
    add_way = models.ForeignKey('add_way',verbose_name='添加方式ID',on_delete='PROTECT')
    server = models.ForeignKey('server',verbose_name='服务器',on_delete='PROTECT')

    class Meta:
        db_table = 'ip_or_api'
        verbose_name = '添加方式'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.id)


class server_api(models.Model):
    api = models.ForeignKey('cloud_api',verbose_name='api',on_delete='PROTECT')
    server = models.ForeignKey('server',verbose_name='sever',on_delete='PROTECT')

    class Meta:
        db_table ='server_api'
        verbose_name = '通过API添加服务器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class server(models.Model):
    # name = models.CharField(blank=False,max_length=100,verbose_name='服务器名称')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete='PROTECT')
    ip = models.GenericIPAddressField(blank=False,max_length=30,unique=True,verbose_name='IP')
    secrect = models.CharField(blank=False,max_length=100,verbose_name='密钥')
    java = models.BooleanField(default=False,verbose_name='Java是否安装')
    java_version = models.CharField(max_length=30,blank=True,verbose_name='Java版本')



    def __str__(self):
        return self.ip


    class Meta:
        db_table = 'server'
        verbose_name = '服务器信息'
        verbose_name_plural = verbose_name


class mc_inf(models.Model):
    name = models.CharField(blank=False,max_length=100,verbose_name='名称')
    server = models.ForeignKey('server',on_delete='PROTECT',verbose_name='所属服务器')

    class Meta:
        db_table = 'mc_inf'
        verbose_name = 'MC信息'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name
