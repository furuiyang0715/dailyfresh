import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

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

        # (5) 获取用户购物车中商品的数目
        cart_count = 0

        # 组织模板上下文
        context = {
            "types": types,
            "goods_banners": goods_banners,
            "goods_promotion": goods_promotion,
            "goods_type": goods_type,
            "cart_count": cart_count,
        }

        print(context)
        for one in goods_promotion:
            print(one.image)
            # print(one.image)

        return render(request, "index.html", context)
