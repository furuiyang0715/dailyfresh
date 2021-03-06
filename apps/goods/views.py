import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner


class IndexView(View):
    """首页"""
    def get(self, request):
        """显示首页"""

        # (1) 获取商品的种类信息
        types = GoodsType.objects.all()

        # (2) 获取轮播商品的信息
        # 需要根据展示的顺序进行排序
        # "index": 默认按照升序排列
        # - "index": 安装降序排列
        goods_banners = IndexGoodsBanner.objects.all().order_by("index")

        # (3) 获取首页促销活动信息
        goods_promotion = IndexPromotionBanner.objects.all().order_by("index")

        # (4) 获取首页分类商品展示信息
        goods_type = IndexTypeGoodsBanner.objects.all()

        for type in types:
            # 每个类型的图片展示行
            image_goods_lst = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1)
            # 每个类型的文字展示行
            text_goods_lst = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0)
            type.image_goods_lst = image_goods_lst
            type.text_goods_lst = text_goods_lst

        # (5) 获取用户购物车中商品的数目
        '''
        在什么时候添加购物车记录? 
        当用户点击加入购物车时需要添加。 
        
        什么时候需要获取购物车记录 ? 
        使用到购物车中数据已经访问购物车页面的时候。 
        
        使用什么存储购物车的记录? 
        redis。 
        
        分析存储购物车记录的格式 ? 
        一个用户的购物车记录成用户的一条数据来进行保存。 
        使用 redis 中的 hash 结构: 
        "cart_用户id": {"sku_id1":商品数目, "sku_id2": 商品数目, ... }
        
        使用 hlen 获取购物车中商品的条目数。 
        
        '''
        user = request.user
        cart_count = 0
        '''
        在 redis 中增加测试数据: 
        hmset cart_39 1 3 2 5 3 2
        '''
        if user.is_authenticated:
            # print("用户已登录")
            conn = get_redis_connection('default')
            cart_key = "cart_{}".format(user.id)
            cart_count = conn.hlen(cart_key)

        # 组织模板上下文
        context = {
            "types": types,
            "goods_banners": goods_banners,
            "goods_promotion": goods_promotion,
            "goods_type": goods_type,
            "cart_count": cart_count,
        }
        return render(request, "index.html", context)

'''
首页要做一个页面静态化: 
如果一个页面经常被访问,但是页面变化得不频繁,或者可以捕捉何时发生改变，那么可以使用页面静态化的技术。 

传统的 django 页面渲染: 
数据库查询数据 --> 数据+模板渲染 --> 返回前端 

使用页面静态化技术: 
在数据发生变化时异步去更新生成新的静态页面 

用户访问时通过 nginx 直接访问生成好的静态文件


'''