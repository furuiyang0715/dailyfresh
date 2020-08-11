import re

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from user.models import User

# from dailyfresh import settings


class RegisterView(View):
    """类视图"""
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        return register_handle(request)


# def register(request):
#     if request.method == "GET":
#         return render(request, "register.html")
#     else:
#         return register_handle(request)


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
    try:
        is_exist = User.objects.get(username=user_name)
    except User.DoesNotExist:   # 在查询不到的时候抛出异常
        is_exist = None
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

    # 发送激活邮件 邮件中含有激活链接。
    # 用户去请求激活链接 激活链接中含有用户的相关信息。
    # 用户去点击了激活邮件，将对应的用户激活。

    # 初步的想法是: 创建一个包含对应用户信息的 url 比如说 /user/active/1 这个 1 表示 user_id
    # 但是如果过于简单，会遭到攻击，盲猜数据对我们的服务器进行访问
    # 所以我们要对用户的身份信息进行加密
    # 安装 pip install itsdangerous
    # 进行导包并进行别名： from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
    # 该类除了加密以及解密 还可以设置加密的过期时间
    # 创建加密对象
    ser = Serializer(settings.SECRET_KEY, 3600)  # 参数分别是秘钥以及以秒为单位的过期时间
    # 对用户信息进行加密
    user_info = {"confirm": user.id}
    ret = ser.dumps(user_info)
    # 拼接激活链接
    active_link = "http://127.0.0.1:8000/user/active?token={}".format(ret)
    # 异步发送激活邮件
    # send_mail(active_link)
    # 注册成功 就跳转到首页
    return redirect(reverse("goods:index"))
