# __author__ = 'Administrator'
#
# api_dict= {
#     'k1':'v1',
#     'k2':'v2',
#     'k3':'v3',
# }
# for k in list(api_dict.keys()):
#     v = api_dict[k]
#     if v == 'v2':
#         del  api_dict[k]
# print(api_dict)
# # for k,v in api_dict.keys():
# #     if v == 'v2':
# #         del api_dict[k]

import rsa
import base64


# ######### 1. 生成公钥私钥 #########
pub_key_obj, priv_key_obj = rsa.newkeys(256)

pub_key_str = pub_key_obj.save_pkcs1()
pub_key_code = base64.standard_b64encode(pub_key_str)

priv_key_str = priv_key_obj.save_pkcs1()
priv_key_code = base64.standard_b64encode(priv_key_str)

print(pub_key_code,type(pub_key_code))
print(priv_key_code,type(priv_key_code))

# ######### 2. 加密 #########
def encrypt(value):
    key_str = base64.standard_b64decode(pub_key_code)
    pk = rsa.PublicKey.load_pkcs1(key_str)
    val = rsa.encrypt(value.encode('utf-8'), pk)
    return val


# ######### 3. 解密 #########
def decrypt(value):
    key_str = base64.standard_b64decode(priv_key_code)
    pk = rsa.PrivateKey.load_pkcs1(key_str)
    val = rsa.decrypt(value, pk)
    return val


# ######### 基本使用 #########
if __name__ == '__main__':
    v = 'wupeiqi'
    v1 = encrypt(v)
    print(v1)
    v2 = decrypt(v1)
    print(v2)

from Crypto.Cipher import AES


