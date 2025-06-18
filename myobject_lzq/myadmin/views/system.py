# 系统管理视图文件
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from collections import defaultdict
from datetime import datetime, timedelta
# Create your views here.
from myadmin.models import 
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.db.models import Avg, Max, Min, Count, Sum
from .forms import 
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay