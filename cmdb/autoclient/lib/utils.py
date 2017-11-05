__author__ = 'Administrator'
from Crypto.Cipher import AES
from lib.conf.config import settings
def encrypt(message):
    """
    数据加密
    :param message:
    :return:
    """
    key = settings.DATA_KEY
    cipher = AES.new(key, AES.MODE_CBC, key)
    ba_data = bytearray(message,encoding='utf-8')  #可变版本的字节
    v1 = len(ba_data)

    #由于AES方法发送的数据长度需要是16的倍数，所以不够16的要补满
    v2 = v1 % 16
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2
    for i in range(v3):
        ba_data.append(v3)  #需要补齐多少就加多少个几 如需补9位就加9个9

    final_data = ba_data.decode('utf-8')
    final_data = final_data.encode('utf-8')  #Python3.6 需要 3.6以下无需
    msg = cipher.encrypt(final_data) # 要加密的字符串，必须是16个字节或16个字节的倍数
    return msg

def decrypt(msg):
    """
    数据解密
    :param message:
    :return:
    """
    from Crypto.Cipher import AES
    key = settings.DATA_KEY
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg) # result = b'\xe8\xa6\x81\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0sdfsd\t\t\t\t\t\t\t\t\t'
    data = result[0:-result[-1]]  #上面补齐了9个9，所以这里真实需要拿到的数据是切片是[0:-9]  其中9由数据的最后一位数据得到，因为补齐的是几个几
    return str(data,encoding='utf-8')


def auth():
    """
    API验证
    :return:
    """
    import time
    import requests
    import hashlib

    ctime = time.time()
    key = "asdfasdfasdfasdf098712sdfs"
    new_key = "%s|%s" %(key,ctime,)

    m = hashlib.md5()
    m.update(bytes(new_key,encoding='utf-8'))  #里面是字节数据
    md5_key = m.hexdigest()                    #返回值是字符串类型

    md5_time_key = "%s|%s" %(md5_key,ctime)

    return md5_time_key

