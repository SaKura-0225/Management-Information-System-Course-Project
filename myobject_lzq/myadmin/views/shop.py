# 店铺信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from myadmin.models import Shop,Orders
from django.core.paginator import Paginator
# from django.db.models import Q
from datetime import datetime
import time
from django.db.models import Avg, Max, Min, Count, Sum
from django.db.models.functions import TruncDate
from collections import defaultdict

def index(request, p_index=1):
    """浏览信息"""
    smod = Shop.objects
    mywhere = []
    slist = smod.filter(status__lt=9)

    ## 查询
    kw = request.GET.get("keyword", None)
    if kw:
        slist = slist.filter(name__contains=kw)
        mywhere.append("keyword="+kw)
    status = request.GET.get('status', '')
    if status != '':
        slist = slist.filter(status=status)
        mywhere.append("status="+status)

    slist = slist.order_by("id")   #对id排序


    # 执行分页处理
    p_index = int(p_index)
    page = Paginator(slist, 20)  # 以每页5条数据分页
    maxpages = page.num_pages  # 获取最大页数
    if p_index > maxpages:
        p_index = maxpages
    if p_index < 1:
        p_index = 1
    list2 = page.page(p_index)  # 获取当前页数据
    plist = page.page_range   # 获取页码列表信息

    slist2 = Orders.objects.values('shop_id').annotate(total_money=Sum('money'))
    slist3 = Orders.objects.all()
    context = {"shop_list": list2, 'plist': plist, 'p_index': p_index, 'max-pages': maxpages, 'mywhere': mywhere,'order_list':slist2,'order_list2':slist3}

    # 显示所有数据代码：
    # context = {"user_list": ulist}
    return render(request, "myadmin/shop/index.html", context)


def add(request):
    """加载信息增加信息"""
    return render(request, "myadmin/shop/add.html")


def insert(request):
    """增加信息"""
    try:
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse("没有店铺封面上传文件信息")
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + cover_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse("没有店铺logo上传文件信息")
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, "wb+")
        for chunk in myfile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        # 实例化model, 封装信息，并执行添加
        ob = Shop()
        ob.name = request.POST["name"]
        ob.address = request.POST["address"]
        ob.phone = request.POST['phone']
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "添加成功"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, sid=0):
    """删除信息"""
    try:
        ob = Shop.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': " 删除成功"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败"}
    return render(request, "myadmin/info.html", context)


def edit(request, sid=0):
    """编辑信息"""
    try:
        ob = Shop.objects.get(id=sid)

        context = {'shop': ob}
        return render(request, "myadmin/shop/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "编辑失败"}
    return render(request, "myadmin/info.html", context)


def update(request, sid=0):
    """更新"""
    try:
        ob = Shop.objects.get(id=sid)
        ob.name = request.POST["name"]
        ob.address = request.POST["address"]
        ob.phone = request.POST['phone']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': " 修改成功"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)
