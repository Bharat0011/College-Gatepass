from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index ,name='index'),
    path('about_us',views.about_us,name='about_us'),
    path('logout',views.logout,name='logout'),
    path('security_login',views.security_login,name='security_login'),
    path('security_home',views.security_home,name='security_home'),
    path('security_in',views.security_in,name='security_in'),
    path('security_out',views.security_out,name='security_out'),
    path('test',views.test,name='test')
]