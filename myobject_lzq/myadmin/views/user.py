# 员工信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from myadmin.models import User1
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.db.models import Avg, Max, Min, Count, Sum


def index(request, p_index=1):
    """浏览信息"""
    umod = User1.objects.all()
    mywhere = []
    ulist = umod.filter(status__lt=9)
    ulist2 = ulist.filter(Q(create_at__istartswith=datetime.now().strftime("%Y-%m-%d")))
    ppp = ulist.aggregate(Count('id'))
    ## 查询
    kw = request.GET.get("keyword", None)
    if kw:
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append("keyword="+kw)
    status = None
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    ulist = ulist.order_by("id")  # 对id排序

    # 执行分页处理
    p_index = int(p_index)
    page = Paginator(ulist, 5)  # 以每页5条数据分页
    maxpages = page.num_pages  # 获取最大页数
    if p_index > maxpages:
        p_index = maxpages
    if p_index < 1:
        p_index = 1
    list2 = page.page(p_index)  # 获取当前页数据
    plist = page.page_range   # 获取页码列表信息
    context = {"user_list": list2, 'o_number': ppp, 'plist': plist, 'p_index': p_index, 'max-pages': maxpages, 'mywhere': mywhere,'selectstatus': status,}
    # 显示所有数据代码：
    #context = {"user_list": ulist}
    return render(request, "myadmin/user/index.html", context)


def add(request):
    """加载信息增加信息"""
    return render(request, "myadmin/user/add.html")


def insert(request):
    """增加信息"""
    try:
        ob = User()
        ob.username = request.POST["username"]
        ob.nickname = request.POST["nickname"]
        # 获取密码并md5
        import hashlib
        import random
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n)
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "添加成功"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    """删除信息"""
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': " 删除成功"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    """编辑信息"""
    try:
        ob = User.objects.get(id=uid)

        context = {'user': ob}
        return render(request, "myadmin/user/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "编辑失败"}
    return render(request, "myadmin/info.html", context)


def update(request, uid=0):
    """更新"""
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': " 修改成功"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)
