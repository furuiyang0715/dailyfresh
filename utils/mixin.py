from django.contrib.auth.decorators import login_required
from django.utils.decorators import classonlymethod


class LoginRequiredMixin(object):
    # 这个类应该位于继承表中最左侧

    @classonlymethod
    def as_view(cls, **initkwargs):
        # 调用父类的方法
        views = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        # 增加登录校验
        return login_required(views)
