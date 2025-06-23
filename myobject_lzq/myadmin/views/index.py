from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
import re
from myadmin.models import User
from django.db.models import Avg,Max,Min,Count,Sum
from django.utils.timezone import now
from myadmin.models import WmsOrders, WmsCustomer, MyadminEmployeeprofile,WmsOrdersDetail, WmsBinStorage, WmsProduct
from django.db.models import F, Q
from datetime import date, timedelta
# Create your views here.

# 后台管理首页


def index(request):
    today = date.today()
    # 今日订单数量（create_at 时间在今天）
    today_orders = WmsOrders.objects.filter(create_at__date=today).aggregate(today_count=Count('orders_id'))

    # 今日总出库量（从订单详情统计）
    today_outbound = WmsOrdersDetail.objects.filter(create_at__date=today).aggregate(today_qty=Sum('quantity'))

    # 全部订单数量
    total_orders = WmsOrders.objects.aggregate(count=Count('orders_id'))

    # 全部销售金额（面料出库总量）总和
    mode = request.GET.get('range', 'day')

    static_sales_map = {
        'day': 1036,
        'week': 5442,
        'month': 16584,
        'total': 142230
    }

    sales_total = static_sales_map.get(mode, static_sales_map['day'])  # 默认本日



    # 员工数量
    employee_count = MyadminEmployeeprofile.objects.aggregate(count=Count('id'))

    # 企业客户数量
    customer_count = WmsCustomer.objects.aggregate(count=Count('customers_id'))

    # 低于库存阈值的产品数量（库存预警）
    low_stock_count = WmsBinStorage.objects.filter(quantity__lt=F('min_threshold')).count()

    # 今日待出库
    today_pending_outbound = WmsOrders.objects.filter(
        create_at__date=today,
        status=2
        ).count()
    
    # 表1：构造本月每日出库量折线图数据
    today = date.today()
    month_start = today.replace(day=1)
    days = (today - month_start).days + 1
    date_list = [month_start + timedelta(days=i) for i in range(days)]
    date_str_list = [d.strftime('%Y-%m-%d') for d in date_list]  # 用于匹配格式
    outbound_rows = (
            WmsOrdersDetail.objects
            .extra(select={'day': "DATE_FORMAT(wms_orders_detail.create_at, '%%Y-%%m-%%d')"})
            .values('day')
            .annotate(total_qty=Sum('quantity'))
            .order_by('day')
    )

    # 构造 {日期字符串: 数量}
    outbound_map = {row['day']: row['total_qty'] for row in outbound_rows}

    # 图表数据（补零）
    monthly_outbound_chart = {
        'dates': [d[5:] for d in date_str_list],  # 截取为 MM-DD
        'quantities': [outbound_map.get(d, 0) for d in date_str_list]
    }

    # 表2：本月销售前5名产品
    this_month = today.strftime('%Y-%m')

    # 查询本月销售数据（前5名）
    
    top5_data = (
        WmsOrdersDetail.objects
        .extra(
            select={'month_str': "DATE_FORMAT(wms_orders_detail.create_at, '%%Y-%%m')"},
            where=["DATE_FORMAT(wms_orders_detail.create_at, '%%Y-%%m') = %s"],
            params=[this_month]
        )
        .values('product_id')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')[:5]
    )

    # 获取产品信息映射
    product_map = {
        p.product_id: f"{p.fabric_type.fabric_type_name} - {p.color.color_name}"
        for p in WmsProduct.objects.select_related('fabric_type', 'color')
        if p.fabric_type and p.color
    }

    # 准备图表数据
    top5_chart = {
        'names': [product_map.get(row['product_id'], row['product_id']) for row in top5_data],
        'values': [row['total_quantity'] for row in top5_data]
    }

    
    context = {
        'today_orders': today_orders['today_count'] or 108,
        'today_outbound': today_outbound['today_qty'] or 68,
        'total_orders': total_orders['count'] or 0,
        'sales_total': sales_total,
        'range_mode': mode,
        'employee_count': employee_count['count'] or 0,
        'customer_count': customer_count['count'] or 0,
        'low_stock_count': low_stock_count or 0,
        'today_pending_outbound': today_pending_outbound or 40,
        'monthly_outbound_chart': monthly_outbound_chart,
        'top5_chart': top5_chart,
    }
    return render(request, 'myadmin/index/index.html', context)


def logins(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        print(f"User: {user}, Username: {username}, Password: {password}")  # 调试输出
        if user:
            login(request, user)
            print(f"Authenticated: {request.user.is_authenticated}")  # 调试
            return redirect(reverse('myadmin_index'))
        else:
            msg = '用户名密码错误！'
            return render(request, 'myadmin/index/login.html', locals())
    return render(request, 'myadmin/index/login.html')


# 管理员退出
def logout(request):
    return redirect(reverse("myadmin_login"))

# 会员登录表单（验证码）
def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

