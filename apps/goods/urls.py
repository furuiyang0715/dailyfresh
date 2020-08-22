from django.conf.urls import url

# from apps.goods import views
from apps.goods.views import IndexView

urlpatterns = [
    # url(r"^$", views.index, name='index'),    # 商品首页
    url(r"^$", IndexView.as_view(), name='index'),    # 商品首页

]
