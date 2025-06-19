
#仓位可视化视图文件
from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.shortcuts import redirect
from django.urls import reverse
import re
from myadmin.models import User
from django.db.models import Avg,Max,Min,Count,Sum


def index(request):
    return render(request, 'myadmin/warehouse/index.html')  
