import re
import traceback

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from user.models import User, Address
from user import tasks

from utils.mixin import LoginRequiredMixin


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

        next_url = request.GET.get("next", reverse("goods:index"))
        response = redirect(next_url)

        is_remembered = request.POST.get("remember")
        if is_remembered:
            response.set_cookie("username", user.username, max_age=7*24*3600)
        else:
            response.delete_cookie('username')

        return response


class LogoutView(View):
    """用户登录视图"""
    def get(self, request):
        # 清除用户的会话数据
        logout(request)
        # 退出后重定向到主页
        return redirect(reverse("goods:index"))


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

class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        # 除了我们传递过去的模板文件之外 django 会将 request.user 也传递过去。
        # request.user 属性是 django 框架拦截请求为其增加的一个属性 无用户信息时该属性为匿名
        # request.user.is_authenticated()   判断用户是否已经登录

        # 在这个页面中需要:(1) 获取用户的个人信息
        # (2) 获取用户的历史浏览记录

        return render(request, 'user_center_info.html', {"page": 'user'})


class UserOrderView(LoginRequiredMixin, View):
# class UserOrderView(View):
    def get(self, request):
        # 获取用户的订单信息
        return render(request, 'user_center_order.html', {'page': 'order'})


class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        # 获取用户的默认地址
        # try:
        #     default_addr = Address.objects.get(user=request.user, is_default=1)
        # except Address.DoesNotExist:
        #     default_addr = None
        default_addr = Address.objects.get_default_address(request.user)

        if not default_addr:
            return render(request, 'user_center_site.html', {"page": "site"})
        else:
            return render(request, 'user_center_site.html', {"page": "site", "default_addr": default_addr})

    def post(self, request):
        '''
        模型字段:
        user = models.ForeignKey('User', verbose_name='所属账户', on_delete=PROTECT)   # 在新版中需要加入 on_delete 参数
        receiver = models.CharField(max_length=20, verbose_name='收件人')
        addr = models.CharField(max_length=256, verbose_name='收件地址')
        zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
        phone = models.CharField(max_length=11, verbose_name='联系电话')
        is_default = models.BooleanField(default=False, verbose_name='是否默认')  # 表明该地址是否是用户的默认地址

        '''
        receiver = request.POST.get("receiver")
        zip_code = request.POST.get("zip_code")
        phone = request.POST.get("phone")
        addr = request.POST.get("addr")

        # 校验数据
        # 校验手机号的正则: ^((13[0-9])|(17[0-1,6-8])|(15[^4,\\D])|(18[0-9]))\d{8}$
        if not all([receiver, addr, phone]):
            return render(request, "user_center_site.html", {"errmsg": "数据不完整"})

        if not re.match("^((13[0-9])|(17[0-1,6-8])|(15[^4,\\D])|(18[0-9]))\d{8}$", phone):
            return render(request, 'user_center_site.html', {"errmsg": "手机号码格式不正确"})

        # 获取登录用户
        user = request.user
        # 查询出当前的默认地址
        # try:
        #     default_addr = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认的收货地址
        #     default_addr = None
        default_addr = Address.objects.get_default_address(user)

        if default_addr:
            is_default = False
        else:
            is_default = True

        # （1） 手动创建
        # address = Address()
        # address.user = request.user   # 地址所属用户是当前登录用户
        # address.receiver = receiver
        # address.zip_code = zip_code
        # address.phone = phone
        # address.addr = addr
        # address.is_default = is_default
        # address.save()

        # （2）调用模型的 create 方法
        address = Address.objects.create(
            user=user,
            receiver=receiver,
            zip_code=zip_code,
            phone=phone,
            addr=addr,
            is_default=is_default,
        )

        # 返回应答：刷新一下地址页面 将设置的默认地址加上去
        # 冲定向是 get 请求
        return redirect(reverse("user:site"))
