from django.test import TestCase
from django.http import JsonResponse
from django.shortcuts import render


# Create your tests here.

def index_chart(request):
    if request.method == "POST":
        datas = [5, 20, 36, 10, 10, 20]
        return JsonResponse({'bar_datas': datas})
    else:
        return render(request, 'index.html')