import json
import ast
from cgitb import reset
from contextlib import nullcontext
import re
from tkinter.messagebox import NO
from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import QueryDict
from .models import Flow
from .models import Meter
from .models import User
from .qos import put_flow, refresh_flow, delete_flow, refresh_meter, put_meter, delete_meter, refresh_topo
#通用视图View
from django.views.generic import View
# Create your views here.

#基于类的视图写法
class login(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            return JsonResponse({"status": "NO", "message":"用户名或密码错误"})
        if(user.password != password):
            return JsonResponse({"status": "NO", "message": "用户名或密码错误"})    
        return JsonResponse({"status": "YES", "message": "登陆成功"})

class register(View):
    def get(self, request):
        return render(request, "register.html")
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        passwordagain = request.POST.get('passwordagain')
        if(len(password)< 6):
            return JsonResponse({"status": "NO", "message": "密码长度过短"})
        if(username == None or password == None):
            return JsonResponse({"status": "NO", "message": "用户名或密码不能为空"})
        if(password != passwordagain):
            return JsonResponse({"status": "NO", "message": "两次密码输入不一致"})
        user = User.objects.filter(username = username)
        if(user.exists()):
            return JsonResponse({"status": "NO", "message": "用户名已存在"})
        try:
            user = User(username = username, password = password)
            user.save()
        except:
            return JsonResponse({"status": "NO", "message": "注册失败"})
        return JsonResponse({"status": "YES", "message": "注册成功"})

class Home(View):
    def get(self, request):
        return render(request, "Home.html")

#拓扑管理模块
class topomanage(View):
    def get(self, request):
        result = refresh_topo()
        return JsonResponse(result)
#流表管理模块
class flowmanage(View):
    def get(self, request):
        #执行刷新流表信息时
        result = refresh_flow()
        return JsonResponse(result)
    def post(self, request):
        #执行添加流表时
        switchID = request.POST.get('switchID')
        flowSet = request.POST.get('flowSet')
        flowSet = json.loads(flowSet)
        flowInfo = {'switchID': switchID, 'flowSet': flowSet}
        result = put_flow(flowInfo)
        return JsonResponse(result, safe = False)
    def delete(self, request):
        data = QueryDict(request.body)
        deleteID = data['deleteID']
        switchID = data['switchID']
        flowlist = Flow.objects.filter(id = deleteID).values()
        flow = flowlist[0]
        flowbasic = flow['basic']
        flowbasic = ast.literal_eval(flowbasic)
        flowID = flowbasic['id'] 
        result = delete_flow(flowID, switchID)
        return JsonResponse(result, safe = False)

#meter表管理模块视图
class metermanage(View):
    def get(self, request):
        #执行刷新meter表信息时
        result = refresh_meter()
        return JsonResponse(result, safe = False)
    def post(self, request):
        #执行添加meter信息时
        switchID = request.POST.get('switchID')
        meterSet = json.loads(request.POST.get('meterSet'))
        meterInfo = {'switchID': switchID, 'meterSet': meterSet} 
        result = put_meter(meterInfo)
        return JsonResponse(result, safe = False)
    def delete(self, request):
        #执行删除meter信息时
        data = QueryDict(request.body)
        deleteID = data['deleteID']
        switchID = data['switchID']
        meterlist = Meter.objects.filter(id = deleteID).values()
        meter = meterlist[0]
        meterbasic = meter['basic']
        meterbasic = ast.literal_eval(meterbasic)
        meterID = meterbasic['meter-id'] 
        result = delete_meter(meterID, switchID)
        return JsonResponse(result, safe = False)
