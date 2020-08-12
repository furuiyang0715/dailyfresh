from django.conf.urls import url

# from apps.user import views
from django.contrib.auth.decorators import login_required

from apps.user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, AddressView

urlpatterns = [
    url(r"^register/$", RegisterView.as_view(), name='register'),    # 将注册改为类视图的使用模式
    # url(r"^register/$", views.register, name='register'),
    # url(r"^register_handle/$", views.register_handle, name='register_handle'),

    # url(r"^active/(?P<token>.*)$", ActiveView.as_view(), name='active'),    # 用户激活 拼接 url 的模式
    url(r"^active/$", ActiveView.as_view(), name='active'),    # 用户激活 将 token 作为参数进行传递

    url(r"^login/$", LoginView.as_view(), name='login'),    # 用户登录

    # login_required 要在视图函数上使用 as_view() 的返回值是函数 所以我们要在这里手动调用一次
    url(r"^$", login_required(UserInfoView.as_view()), name='info'),    # info
    url(r"^order/$", UserOrderView.as_view(), name='order'),    # order
    url(r"^site/$", AddressView.as_view(), name='site'),    # site


]
