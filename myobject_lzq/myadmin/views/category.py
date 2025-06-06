# 菜品类别管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
from myadmin.models import Category, Shop
from django.core.paginator import Paginator
from datetime import datetime


def index(request, p_index=1):
    """浏览信息"""
    umod = Category.objects
    mywhere = []
    ulist = umod.filter(status__lt=9)

    ## 查询
    kw = request.GET.get("keyword", None)
    if kw:
        ulist = ulist.filter(name__contains=kw)
        mywhere.append("keyword="+kw)
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    ulist = ulist.order_by("id")  # 对id排序

    # 执行分页处理
    p_index = int(p_index)
    page = Paginator(ulist, 40)  # 以每页5条数据分页
    maxpages = page.num_pages  # 获取最大页数
    if p_index > maxpages:
        p_index = maxpages
    if p_index < 1:
        p_index = 1
    list2 = page.page(p_index)  # 获取当前页数据
    plist = page.page_range   # 获取页码列表信息

    # 遍历当前菜品分类信息并封装对应的店铺信息
    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name
    context = {"category_list": list2, 'plist': plist, 'p_index': p_index, 'max-pages': maxpages, 'mywhere': mywhere}

    # 显示所有数据代码：
    # context = {"user_list": ulist}
    return render(request, "myadmin/category/index.html", context)


def loadCategory(request, sid):
    clist = Category.objects.filter(status__lt=9, shop_id=sid).values("id", "name")
    # 返回querset对象，使用list强转成对应菜品分类列表信息
    return JsonResponse({'data': list(clist)})

def add(request):
    """加载信息增加信息"""
    # 获取当前所有店铺信息
    slist = Shop.objects.values("id", 'name')
    slist = slist.filter(status__lt=9)
    context = {"shoplist": slist}
    return render(request, "myadmin/category/add.html", context)


def insert(request):
    """增加信息"""
    try:
        ob = Category()
        ob.shop_id = request.POST["shop_id"]
        ob.name = request.POST["name"]
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "添加成功"}
    except Exception as err:
        print(err)
        context = {'info': "添加失败"}
    return render(request, "myadmin/info.html", context)


def delete(request, cid=0):
    """删除信息"""
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': " 删除成功"}
    except Exception as err:
        print(err)
        context = {'info': "删除失败"}
    return render(request, "myadmin/info.html", context)


def edit(request, cid=0):
    """编辑信息"""
    try:
        # 获取当前所有店铺信息
        ob = Category.objects.get(id=cid)
        context = {'category': ob}
        slist = Shop.objects.values("id", 'name')
        slist = slist.filter(status__lt=9)
        context["shoplist"] = slist
        return render(request, "myadmin/category/edit.html", context)
    except Exception as err:
        print(err)
        context = {'info': "编辑失败"}
    return render(request, "myadmin/info.html", context)


def update(request, cid=0):
    """更新"""
    try:
        ob = Category.objects.get(id=cid)
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': " 修改成功"}
    except Exception as err:
        print(err)
        context = {'info': "修改失败"}
    return render(request, "myadmin/info.html", context)
