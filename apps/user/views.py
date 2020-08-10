from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def register(request):
    return render(request, "register.html")


def register_handle(request):
    # 接收数据

    # 校验数据

    # 进行业务逻辑处理

    # 返回应答

    #
    return HttpResponse("注册成功")
