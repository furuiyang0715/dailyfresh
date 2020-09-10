from celery import task
from django.conf import settings
from django.core.mail import send_mail
from django_redis import get_redis_connection
from flask import request

from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner


@task
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

@task
def generate_static_index_html():
    """生成静态主页的任务"""
    types = GoodsType.objects.all()
    goods_banners = IndexGoodsBanner.objects.all().order_by("index")
    goods_promotion = IndexPromotionBanner.objects.all().order_by("index")
    goods_type = IndexTypeGoodsBanner.objects.all()

    for type in types:
        image_goods_lst = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1)
        text_goods_lst = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0)
        type.image_goods_lst = image_goods_lst
        type.text_goods_lst = text_goods_lst
    user = request.user
    cart_count = 0

    if user.is_authenticated:
        conn = get_redis_connection('default')
        cart_key = "cart_{}".format(user.id)
        cart_count = conn.hlen(cart_key)

    context = {
        "types": types,
        "goods_banners": goods_banners,
        "goods_promotion": goods_promotion,
        "goods_type": goods_type,
        "cart_count": cart_count,
    }
    # return render(request, "index.html", context)
