from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import PROTECT

from db.base_model import BaseModel


class User(AbstractUser, BaseModel):
    """用户模型类"""
    class Meta:
        db_table = 'df_user'   # 在数据库中存在的表名
        verbose_name = '用户'  # 在后台单数时显示的名称
        verbose_name_plural = verbose_name   # 在后台时复数显示的名称


class AddressManager(models.Manager):
    """自定义的一个模型管理器对象"""
    def get_default_address(self, user):
        """获取用户的默认地址"""
        # 使用 self.model 获取当前模型管理器的模型类
        try:
            default_addr = self.get(user=user, is_default=True)
            # default_addr = self.model.objects.get(user=user, is_default=True)
            # default_addr = Address.objects.get(user=user, is_default=True)
        except self.model.DoesNotExist:
            default_addr = None
        return default_addr


class Address(BaseModel):
    """地址模型类"""
    # user = models.ForeignKey('User', verbose_name='所属账户')   # 用户和地址是一对多的关系 在多的一方用 foreiginkey 链接一的一方
    user = models.ForeignKey('User', verbose_name='所属账户', on_delete=PROTECT)   # 在新版中需要加入 on_delete 参数
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')  # 表明该地址是否是用户的默认地址

    # 使用自定义的模型管理器对象
    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name
