import os

from celery import task
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django_redis import get_redis_connection
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

    # user = request.user
    # cart_count = 0
    # if user.is_authenticated:
    #     conn = get_redis_connection('default')
    #     cart_key = "cart_{}".format(user.id)
    #     cart_count = conn.hlen(cart_key)

    # (1) 组织模板上下文
    context = {
        "types": types,
        "goods_banners": goods_banners,
        "goods_promotion": goods_promotion,
        "goods_type": goods_type,
        # "cart_count": cart_count,
    }
    # (2) 加载模板 返回模板对象
    temp = loader.get_template("static_index.html")
    # (3) 渲染模板
    static_index_html = temp.render(context)
    # (4) 生成首页对应的静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)


'''在终端测试 运行任务 生成首页
>>> from user.tasks import generate_static_index_html 
>>> generate_static_index_html.delay() 
<AsyncResult: 7efe522c-21fc-4b3d-ac0d-60e943ca1287>

'''