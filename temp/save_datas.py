# coding=utf8
import datetime
import sys

from temp.base_spider import SpiderBase


class SaveDatas(SpiderBase):
    def make_type_datas(self):
        self._test_init()
        fields = ['id', 'create_time', 'update_time', 'is_delete', 'name', 'logo', 'image']
        datas = [
            (1, '2017-11-14 05:02:09.888544', '2017-11-14 05:02:09.888598', 0, '新鲜水果', 'fruit', 'images/banner01.jpg'),
            (2, '2017-11-14 05:04:32.069517', '2017-11-14 05:04:32.069561', 0, '海鲜水产', 'seafood', 'images/banner02.jpg'),
            (3, '2017-11-14 05:05:34.514415', '2017-11-14 05:05:34.514449', 0, '猪牛羊肉', 'meet', 'images/banner03.jpg'),
            (4, '2017-11-14 05:05:58.366135', '2017-11-14 05:05:58.366170', 0, '禽类蛋品', 'egg', 'images/banner04.jpg'),
            (5, '2017-11-14 05:06:32.561861', '2017-11-14 05:06:32.561895', 0, '新鲜蔬菜', 'vegetables', 'images/banner05.jpg'),
            (6, '2017-11-14 05:06:55.562634', '2017-11-14 05:06:55.562673', 0, '速冻食品', 'ice', 'images/banner06.jpg'),
        ]
        for data in datas:
            item = dict(zip(fields, data))
            self._save(self.test_client, item, 'df_goods_type', fields)

    def make_sku_goods_datas(self):
        self._test_init()
        fields = ['id', 'create_time', 'update_time', 'is_delete',
                  'name', 'desc', 'price', 'unite', 'image', 'stock',
                  'sales', 'status', 'goods_id', 'type_id']
        datas = [
            (1, '2017-11-15 03:10:14.045538', '2017-11-14 08:24:49.138489', 0, '草莓 500g', '草莓简介', 10.00, '500g', 'images/goods/caomei.jpg', 98, 0, 1, 1, 1),
            (2, '2017-11-15 03:11:04.490384', '2017-11-14 08:44:43.484243', 0, '盒装草莓', '草莓简介', 20.00, '盒', 'images/goods/hecaomei.jpg',10, 0, 1, 1, 1),
            (3, '2017-11-15 03:12:32.165020', '2017-11-14 08:25:22.505620', 0, '葡萄', '葡萄简介', 20.00, '500g', 'images/goods/putao.jpg', 7, 0, 1, 2, 1),
            (4, '2017-11-15 03:13:16.457844', '2017-11-14 08:25:34.181904', 0, '柠檬', '简介', 32.00, '500g', 'images/goods/ningmeng.jpg', 12, 0, 1, 3, 1),
            (5, '2017-11-15 03:14:05.799352', '2017-11-14 08:25:56.427676', 0, '奇异果', '简介', 12.12, '500g', 'images/goods/qiyiguo.jpg', 12, 0, 1, 4, 1),
            (26, '2017-11-14 08:53:00.188619', '2017-11-14 08:53:00.188652', 0, '越南芒果', '新鲜越南芒果', 29.90, '2.5kg', 'images/goods/mangguo.jpg', 100, 0, 1, 25, 1),
            (6, '2017-11-15 03:15:09.971968', '2017-11-14 08:26:09.113586', 0, '大青虾', '简介', 34.00, '500g', 'images/goods/qingxia.jpg', 12, 0, 1, 5, 2),
            (7, '2017-11-15 03:15:53.812181', '2017-11-14 08:26:19.094675', 0, '北海道秋刀鱼', '简介', 50.00, '500g', 'images/goods/qiudaoyu.jpg', 15, 0, 1, 6, 2),
            (8, '2017-11-15 03:16:24.763232', '2017-11-14 08:26:31.121824', 0, '扇贝', '简介', 56.60, '500g', 'images/goods/shanbei.jpg', 13, 0, 1, 7, 2),
            (9, '2017-11-15 03:17:13.426611', '2017-11-14 08:26:58.739624', 0, '基围虾','简介', 100.90, '500g', 'images/goods/jiweixia.jpg', 14, 0, 1, 8, 2),
            (10, '2017-11-15 03:17:47.656066', '2017-11-14 08:29:56.158261', 0, '猪肉','简介', 23.99, '500g', 'images/goods/pig.jpg', 100, 0, 1, 9, 3),
            (11, '2017-11-15 03:18:15.497630', '2017-11-14 08:31:27.169999', 0, '牛肉','简介', 34.99, '500g', 'images/goods/beef.jpg', 100, 0, 1, 10, 3),
            (12, '2017-11-15 03:18:44.453933', '2017-11-14 08:32:22.493340', 0, '羊肉','简介', 56.99, '500g', 'images/goods/yangrou.jpg', 100, 0, 1, 11, 3),
            (13, '2017-11-15 03:19:10.209472', '2017-11-14 08:33:15.061544', 0, '牛排','简介', 99.99, '500g', 'images/goods/niupai.jpg',100, 0, 1, 12, 3),
            (14, '2017-11-15 03:19:44.020204', '2017-11-14 08:34:31.275370', 0, '盒装鸡蛋', '简介', 23.00,'500g', 'images/goods/geegg.jpg', 100, 0, 1, 13, 4),
            (15, '2017-11-15 03:20:20.962831', '2017-11-14 08:35:21.725162', 0, '鸡肉', '简介', 32.00, '500g', 'images/goods/jirou.jpg', 100, 0, 1, 14, 4),
            (16, '2017-11-15 03:20:53.724305', '2017-11-14 08:37:27.336911', 0, '鸭蛋', '简介', 45.00, '盒', 'images/goods/yadan.jpg', 121, 0, 1, 15, 4),
            (17, '2017-11-15 03:21:22.965398', '2017-11-14 08:38:08.440778', 0, '鸡腿', '简介', 45.00, '500g','images/goods/jitui.jpg',12, 0, 1, 16, 4),
            (27, '2017-11-17 07:57:00.677981', '2017-11-17 07:57:00.678022', 0, '鹌鹑蛋', '简介', 39.80, '126枚','images/goods/andan.jpg', 100, 0, 1, 26, 4),
            (28, '2017-11-17 07:58:18.361078',  '2017-11-17 07:58:18.361122', 0, '鹅蛋', '简介', 49.90, '6枚', 'images/goods/edan.jpg', 80, 0, 1, 27, 4),
            (18, '2017-11-15 03:22:04.462490', '2017-11-14 08:38:45.119926', 0, '白菜', '简介', 4.50, '500g', 'images/goods/baicai.jpg', 100, 0, 1, 17, 5),
            (19, '2017-11-15 03:22:31.745392', '2017-11-14 08:39:40.030728', 0, '芹菜', '简介', 3.50, '500g', 'images/goods/qincai.jpg',12, 0, 1, 18, 5),
            (20, '2017-11-15 03:23:21.161526', '2017-11-14 08:40:08.185684', 0, '香菜', '简介', 7.90, '500g',  'images/goods/xiangcai.jpg', 100, 0, 1, 19, 5),
            (21, '2017-11-15 03:23:46.986158', '2017-11-14 08:40:38.330247', 0, '冬瓜', '简介', 12.99, '500g', 'images/goods/donggua.jpg',100, 0, 1, 20, 5),
            (29, '2017-11-17 07:59:48.998394', '2017-11-17 07:59:48.998431', 0, '红辣椒', '简介', 11.00, '2.5kg', 'images/goods/lajiao.jpg', 150, 0, 1, 28, 5),
            (22, '2017-11-15 03:24:10.445214', '2017-11-14 08:41:19.155821', 0, '鱼丸', '简介', 66.00, '500g', 'images/goods/yuwan.jpg', 12, 0, 1, 21, 6),
            (23, '2017-11-15 03:24:37.927158', '2017-11-14 08:41:59.658787', 0, '蟹棒', '简介', 68.00, '500g', 'images/goods/xiebang.jpg', 100, 0, 1, 22, 6),
            (24, '2017-11-15 03:25:18.235816', '2017-11-14 08:42:25.868409', 0, '虾丸', '简介', 89.99, '500g', 'images/goods/xiawan.jpg', 100, 0, 1, 23, 6),
            (25, '2017-11-15 03:25:56.170531', '2017-11-14 08:43:18.768380', 0, '速冻水饺', '简介', 20.00, '袋', 'images/goods/shuijiao.jpg', 100, 0, 1, 24, 6),
        ]

        for data in datas:
            item = dict(zip(fields, data))
            self._save(self.test_client, item, 'df_goods_sku', fields)

    def start(self):
        # SaveDatas().make_type_datas()
        SaveDatas().make_sku_goods_datas()


if __name__ == '__main__':
    SaveDatas().start()
