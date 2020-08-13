# 校验手机号的正则表达式
import re
partten = '^((13[0-9])|(17[0-1,6-8])|(15[^4,\\D])|(18[0-9]))\d{8}$'
ret1 = re.match(partten, "1908jjj")
ret2 = re.match(partten, "15626046299")
print(ret1)
print(ret2)
