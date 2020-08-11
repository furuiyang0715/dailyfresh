from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
ser = Serializer("my_key", 3600)   # 参数分别是秘钥以及以秒为单位的过期时间
print(ser)
# 我想要传递的信息
info = {"confirm": 1}
# 加密
en_info = ser.dumps(info)
print(en_info)
en_info2 = en_info.decode()
print(en_info2)
# 解密
# 说明解密的时候 输入 bytes 以及 str 均可
de_info = ser.loads(en_info)
print(de_info)
de_info2 = ser.loads(en_info2)
print(de_info2)


# from django.conf import settings
# print(settings)
