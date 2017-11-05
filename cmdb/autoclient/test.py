import traceback

# def func():
#     try:
#         i = 123
#         for i in range(10):
#             pass
#         int('asdfasdf')
#     except Exception as e:
#         print(traceback.format_exc())
# #
# # func()
#
#
# # 100任务
# import time
# from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
#
# def task(i):
#     time.sleep(1)
#     print(i)
#
# p = ThreadPoolExecutor(10)
# for row in range(100):
#     p.submit(task,row)
#
# import requests
# response = requests.get("http://127.0.0.1:8000/api/asset.html")
# print(response.text)

# ############### a. 发令牌: 静态 ###############
# import requests
# key = "asdfasdfasdfasdf098712sdfs"
# response = requests.get("http://127.0.0.1:8000/api/asset.html",headers={'OpenKey':key})
# print(response.text)

# ############### b. 改良: 动态令牌, ###############
# import time
# import requests
# import hashlib
#
# ctime = time.time()
# key = "asdfasdfasdfasdf098712sdfs"
# new_key = "%s|%s" %(key,ctime,)
#
# m = hashlib.md5()
# m.update(bytes(new_key,encoding='utf-8'))
# md5_key = m.hexdigest()
#
# md5_time_key = "%s|%s" %(md5_key,ctime)
#
# print(md5_time_key)
# response = requests.get("http://127.0.0.1:8000/api/asset.html",headers={'OpenKey':md5_time_key})
# print(response.text)

import requests
import rsa
import base64
import json

server_info = {'host':'xxx','disk':['11,22','456']}


# ######### 2. 加密 #########
def encrypt(value):
    PUB_KEY = b'LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tCk1DZ0NJUUN2Q0p3anllTTUwc3FUMGVXNHpEVXFGNllDS01QanlUVW56TFptSW5OeUR3SURBUUFCCi0tLS0tRU5EIFJTQSBQVUJMSUMgS0VZLS0tLS0K'
    key_str = base64.standard_b64decode(PUB_KEY)
    pk = rsa.PublicKey.load_pkcs1(key_str)
    val = rsa.encrypt(value.encode('utf-8'), pk)
    return val

value = json.dumps(server_info,ensure_ascii=True)
print(value,type(value))
result = encrypt("xxxxxx")
print(result)

# requests.post(url='http://127.0.0.1:8000/api/asset.html',json=server_info)











