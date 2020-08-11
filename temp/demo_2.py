from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
ser = Serializer("my_key", 3600)   # 参数分别是秘钥以及以秒为单位的过期时间
print(ser)
# 我想要传递的信息
info = {"confirm": 1}
# 加密
en_info = ser.dumps(info)
print(en_info)
# 解密
de_info = ser.loads(en_info)
print(de_info)


# from django.conf import settings
# print(settings)
