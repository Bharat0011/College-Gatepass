from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index ,name='index'),
    path('about_us',views.about_us,name='about_us'),
    path('logout',views.logout,name='logout'),
    path('principal_login',views.principal_login,name='principal_login'),
    path('principal_home',views.principal_home,name='principal_home'),
    path('principal_stud_data',views.principal_stud_data,name='principal_stud_data'),
    path('stu_report',views.stu_report,name='stu_report'),
    path('frequent_app',views.frequent_app,name='frequent_app')
]