from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def register(request):
    return render(request, "register.html")


def register_handle(request):
    # 接收数据
    print(request.POST)
    user_name = request.POST.get("user_name")
    password = request.POST.get("pwd")
    email = request.POST.get("email")
    # print(user_name)
    # print(password)
    # print(email)


    # 校验数据

    # 进行业务逻辑处理

    # 返回应答

    #
    return HttpResponse("注册成功")
