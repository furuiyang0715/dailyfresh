
import re
email = '15626046299@163.com'
email ='2564493603@qq.com'
ret = re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email)
print(ret)