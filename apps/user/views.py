import re
import traceback

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from user.models import User
from user import tasks


class RegisterView(View):
    """类视图"""
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        return register_handle(request)


def register_handle(request):
    # 接收数据
    user_name = request.POST.get("user_name")
    password = request.POST.get("pwd")
    email = request.POST.get("email")

    # 校验数据
    if not all([user_name, password, email]):
        return render(request, "register.html", {"errmsg": '数据不完整'})

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
    ret = ser.dumps(user_info)   # bytes类型的
    token = ret.decode("utf-8")  # 进一步编码
    # 拼接激活链接
    active_link = "http://127.0.0.1:8000/user/active?token={}".format(token)
    # 这一步骤是将信息发送给 smtp 服务器 然后再由其转发给用户邮箱
    # 若直接同步发送 会造成用户页面阻塞 用户体验不佳

    # 我们应该将这个任务放到后台去异步执行
    # 使用 djcelery 的启动:  python manage.py celery worker --loglevel=info
    # 调用示例: tasks.my_send_mail.delay()

    # my_send_mail(active_link, user.email)   # 使用同步发送
    tasks.my_send_mail.delay(active_link, user.email)   # 使用 djcelery 的配置

    return HttpResponse("注册成功 请到邮箱激活登录")


class ActiveView(View):
    """用户激活视图"""
    def get(self, request):
        token = request.GET.get("token")    # 这里我没有拼接 url 而是将 token 作为参数进行传递
        token = token.encode("utf-8")
        ser = Serializer(settings.SECRET_KEY, 3600)
        try:
            user_info = ser.loads(token)
        except SignatureExpired:
            return HttpResponse("激活链接已超时")
        except:
            err_msg = traceback.format_exc()
            return HttpResponse("激活失效: {}".format(err_msg))
        else:
            # 激活成功
            user_id = user_info.get("confirm")
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            # 跳转到登录页面
            return redirect(reverse("user:login"))


class LoginView(View):
    """用户登录视图"""
    def get(self, request):
        # 判断用户是否勾选了记住用户名
        if "username" in request.COOKIES:
            user_name = request.COOKIES.get("username")
        else:
            user_name = ''
        return render(request, "login.html", {"username": user_name,
                                              # 'checked': checked,
                                              })

    def post(self, request):
        user_name = request.POST.get("username")
        pass_word = request.POST.get("pwd")

        # 校验数据的完整性
        # 这一步前端以及后端都需要进行处理
        if not all([user_name, pass_word]):
            return render(request, 'login.html', {"errmsg": "数据不完整"})

        # # 手动去查询用户是否存在
        # 这样不成功的原因是 数据库中的密码 在入库时 已经经过了加密处理
        # try:
        #     user = User.objects.get(username=user_name, password=pass_word)
        # except:
        #     user = None

        # 在其中已经完成了将密码进行加密后的比较
        user = authenticate(username=user_name, password=pass_word)

        # 检验密码是否正确
        if not user:
            return render(request, 'login.html', {"errmsg": "用户不存在或者密码错误"})
        elif not user.is_active:
            return render(request, 'login.html', {"errmsg": "用户尚未激活"})

        # 跳转到主页

        # 记录用户的登录状态 手动的
        # request.session['is_login'] = 1

        # 使用 django_redis
        # 安装:pip install django-redis

        # 使用封装好的方法
        login(request, user)

        response = redirect(reverse("goods:index"))

        # 判断是否需要记住用户名
        is_remembered = request.POST.get("remember")
        print("####### ", is_remembered)

        if is_remembered:
            print("设置 cookie ")
            response.set_cookie("username", user.username, max_age=7*24*3600)
        else:
            response.delete_cookie('username')

        return response


def my_send_mail(msg, user_email):
    '''
    msg: 需要发送的信息
    user_email: 用户填写的接收激活信息的邮箱
    '''
    send_mail("dailyfrsh 用户注册",
              '',
              settings.EMAIL_FROM,
              [user_email],
              html_message=msg
              )


# https://docs.djangoproject.com/zh-hans/3.0/topics/auth/default/#django.contrib.auth.decorators.login_required
# 使用 login_required 装饰器 视图函数可用

class UserInfoView(View):
    def get(self, request):
        return render(request, 'user_center_info.html', {"page": 'user'})


class UserOrderView(View):
    def get(self, request):
        return render(request, 'user_center_order.html', {'page': 'order'})


class AddressView(View):
    def get(self, request):
        return render(request, 'user_center_site.html', {"page": "site"})
