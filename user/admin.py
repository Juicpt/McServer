from django.contrib import admin
from .models import cloud_api,add_way,ip_or_api,server_api,server,mc_inf
# Register your models here.

admin.site.register(cloud_api)
admin.site.register(add_way)
admin.site.register(ip_or_api)
admin.site.register(server_api)
admin.site.register(server)
admin.site.register(mc_inf)