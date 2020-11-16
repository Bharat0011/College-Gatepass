from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index ,name='index'),
    path('about_us',views.about_us,name='about_us'),
    path('gfm_login',views.gfm_login,name='gfm_login'),
    path('gfm_home',views.gfm_home,name='gfm_home'),
    path('gfm_validate_stu',views.gfm_validate_stu,name='gfm_validate_stu'),
    path('gfm_signup_form',views.gfm_signup_form,name='gfm_signup_form'),
    path('gfm_grant_permission',views.gfm_grant_permission,name='gfm_grant_permission'),
    path('gfm_rejected_stu',views.gfm_rejected_stu,name='gfm_rejected_stu'),
    path('forget_pass1',views.forget_pass1,name='forget_pass1'),
    path('forget_pass2',views.forget_pass,name='forget_pass'),
    path('gfm_stu_report',views.gfm_stu_report,name='gfm_stu_report'),
    path('gfm_stu_profile',views.gfm_stu_profile,name='gfm_stu_profile'),
    path('edit_myprof',views.edit_myprof,name='edit_myprof'),
    path('logout',views.logout,name='logout'),
    
]