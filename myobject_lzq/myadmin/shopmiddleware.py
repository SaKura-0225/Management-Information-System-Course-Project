
# 自定义中间件类
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.middleware import AuthenticationMiddleware
import re


class ShopMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("ShopMiddleware")

    def __call__(self, request):

        # 获取当前请求路径
        path = request.path
        # print("mycall..."+path)

        # 后台请求路由判断
        # 定义网站后台不用登录也可访问的路由url
        #urllist = []
        urllist = ['/myadmin/login', '/myadmin/dologin', '/myadmin/logout', '/myadmin/verify']
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if re.match(r'^/myadmin', path) and (path not in urllist):
            # 检查是否登录
            if not request.user.is_authenticated:
                # 执行登录界面跳转
                return redirect(reverse('myadmin_login'))


        # 判断大堂点餐请求，是否登录（session中是否有webuser)
        if re.match(r'^/web', path):
            if not request.user.is_authenticated:
                # 执行登录界面跳转
                return redirect(reverse('web_login'))



        # 请求继续执行下去
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
