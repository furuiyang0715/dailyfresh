from celery import task
from django.conf import settings
from django.core.mail import send_mail


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
