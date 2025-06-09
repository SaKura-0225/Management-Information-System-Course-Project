
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect

# 用户登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        # 用authenticate判断用户名密码是否正确
        if user:
            login(request,user)
            return redirect('/')
        else:
            msg='用户名密码错误！'
            return render(request,'myadmin/index/login.html',locals())
    return render(request,'myadmin/index/index.html')