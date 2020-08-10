import re

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def register(request):
    return render(request, "register.html")


def register_handle(request):
    # 接收数据
    # print(request.POST)
    user_name = request.POST.get("user_name")
    password = request.POST.get("pwd")
    email = request.POST.get("email")
    # print(user_name)
    # print(password)
    # print(email)

    # 校验数据
    if not all([user_name, password, email]):
        return render(request, "register.html", {"errmsg": '数据不完整'})

    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, "register.html", {"errmsg": '邮箱格式不正确'})

    if not request.POST.get("allow") == "on":
        return render(request, "register.html", {"errmsg": '请先同意用户协议'})

    # 进行业务逻辑处理

    # 返回应答

    #
    return HttpResponse("注册成功")
