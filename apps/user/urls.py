from django.conf.urls import url

# from apps.user import views
from apps.user.views import RegisterView

urlpatterns = [
    url(r"^register/$", RegisterView.as_view(), name='register'),    # 将注册改为类视图的使用模式
    # url(r"^register/$", views.register, name='register'),
    # url(r"^register_handle/$", views.register_handle, name='register_handle'),

]
