import re
from django.shortcuts import render, redirect
from django.urls import reverse
from user.models import User


def register(request):
    return render(request, "register.html")


def register_handle(request):
    # 接收数据
    user_name = request.POST.get("user_name")
    password = request.POST.get("pwd")
    email = request.POST.get("email")

    # 校验数据
    if not all([user_name, password, email]):
        return render(request, "register.html", {"errmsg": '数据不完整'})

    # if user_name == 'aaa':
    #     return render(request, "register.html", {"errmsg": 'Just for test'})

    # 校验用户名是否重复
    is_exist = User.objects.get(username=user_name)
    if is_exist:
        return render(request, "register.html", {"errmsg": '该用户名已存在'})

    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, "register.html", {"errmsg": '邮箱格式不正确'})

    if not request.POST.get("allow") == "on":
        return render(request, "register.html", {"errmsg": '请先同意用户协议'})

    # 进行业务逻辑处理
    user = User.objects.create_user(user_name, email, password)
    # 默认用户是激活的 在此修改新注册用户为未激活状态 后续需要通过邮箱、短信等激活
    user.is_active = 0
    # 作出更改时，要调用 save 将更改保存下来
    user.save()

    # 注册成功 就跳转到首页
    return redirect(reverse("goods:index"))
