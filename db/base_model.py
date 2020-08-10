"""模型抽象基类"""
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        # 说明 BaseModel 是一个抽象模型类
        abstract = True
