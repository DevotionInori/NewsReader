from django.shortcuts import render
from django.http import HttpResponse

def home(resquest):#定义一个函数，第一个参数必须是request
    return render(resquest, 'home.html')