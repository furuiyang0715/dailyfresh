from django.conf.urls import url

# from apps.user import views
from apps.user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, AddressView

urlpatterns = [
    url(r"^register/$", RegisterView.as_view(), name='register'),    # 将注册改为类视图的使用模式
    # url(r"^register/$", views.register, name='register'),
    # url(r"^register_handle/$", views.register_handle, name='register_handle'),

    # url(r"^active/(?P<token>.*)$", ActiveView.as_view(), name='active'),    # 用户激活 拼接 url 的模式
    url(r"^active/$", ActiveView.as_view(), name='active'),    # 用户激活 将 token 作为参数进行传递

    url(r"^login/$", LoginView.as_view(), name='login'),    # 用户登录

    url(r"^info/$", UserInfoView.as_view(), name='login'),    # info
    url(r"^order/$", UserOrderView.as_view(), name='login'),    # order
    url(r"^site/$", AddressView.as_view(), name='login'),    # site



]
