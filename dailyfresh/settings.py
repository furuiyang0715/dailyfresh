"""
Django settings for dailyfresh project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys

import configs
from configs import TEST_MYSQL_DB, TEST_MYSQL_USER, TEST_MYSQL_PASSWORD, TEST_MYSQL_HOST, TEST_MYSQL_PORT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将 apps 添加到路径中
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6k=kbx8dea#*#7bw=c7cem9z6v+f@wh$7a&*%6%vpf$-@ies^='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 注册 my apps
    'user',   # 用户模块
    'goods',  # 商品模块
    'cart',   # 购物车模块
    'order',  # 订单模块
    # 添加富文本编辑器组件
    'tinymce',

    'djcelery',
]

# 写入富文本编辑器的配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dailyfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dailyfresh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': TEST_MYSQL_DB,
        'USER': TEST_MYSQL_USER,
        'PASSWORD': TEST_MYSQL_PASSWORD,
        'HOST': TEST_MYSQL_HOST,
        'PORT': TEST_MYSQL_PORT,

        # 'OPTIONS': {
        #     # 存储引擎启用严格模式，非法数据值被拒绝
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        #     'charset': 'utf8mb4',
        # },
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# 将时区进行本地化
LANGUAGE_CODE = 'zh-hans'  # 使用中国语言
TIME_ZONE = 'Asia/Shanghai'  # 使用中国上海时间

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# 配置的静态文件的查找路径
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]


# 不在使用系统的用户模型类 而是使用我们自己的用户模型类
# 配置 django 认证系统使用的模型类 不再生成 auth_user 表
AUTH_USER_MODEL = "user.User"

# 发送邮件的配置
# 邮件服务后端
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = '15626046299@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = configs.EMAIL_HOST_PASSWORD
# 收件人看到的发件人
EMAIL_FROM = 'mydailyfresh<15626046299@163.com>'    # 尖括号内的邮箱必须和上面的邮箱地址一致 否则发送不出去


import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/2'

# session 的配置
# （1） 存储在数据库中 属于默认的存储方式
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# （2） 存储在 内存中
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# （3）混合存储 先从内存中获取 不存在则从数据库中获取
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
'''
依赖于Cookie
所有请求者的Session都会存储在服务器中，服务器如何区分请求者和Session数据的对应关系呢？
答：在使用Session后，会在Cookie中存储一个sessionid的数据，每次请求时浏览器都会将这个数据发给服务器，服务器在接收到sessionid后，会根据这个值找出这个请求者的Session。
结果：如果想使用Session，浏览器必须支持Cookie，否则就无法使用Session了。
存储Session时，键与Cookie中的sessionid相同，值是开发人员设置的键值对信息，进行了base64编码，过期时间由开发人员设置。 
'''


# 使用 django-redis 时配置用户缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "mysecret"
        }
    }
}
# session 是存储在缓存中 缓存是基于 redis 存储
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# 未登录的默认跳转地址
LOGIN_URL = '/user/login/'
