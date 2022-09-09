from atexit import register
from django.contrib import admin
from django.urls import path
from .views import login, register, Home, flowmanage, metermanage, topomanage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login.as_view()),
    path('QoS', Home.as_view()),
    path('login',login.as_view()),
    path('register',register.as_view()),
    path('topo/get', topomanage.as_view()),
    path('flow/get', flowmanage.as_view()),
    path('flow/post', flowmanage.as_view()),
    path('flow/delete', flowmanage.as_view()),
    path('meter/get', metermanage.as_view()),
    path('meter/post',metermanage.as_view()),
    path('meter/delete',metermanage.as_view()),
]
