"""mc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from user.views import LoginView,LogoutView,HomeView
from server.views import game,setting,java,add_game,game_inf,profile,cmd


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('', HomeView.as_view(), name='index'),
    path('game/', game.as_view(), name='game'),
    path('game/<int:id>/', add_game.as_view(),name = 'add_game'),
    path('game/<int:id>/profile/',profile.as_view(),name='profile'),
    path('game/<int:id>/command/',cmd.as_view(), name='command'),
    path('setting/', setting.as_view(), name='setting'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('java/',java.as_view(),name='java'),
    path('game_inf/',game_inf.as_view(),name='game_inf')


]
