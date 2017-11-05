import json
import hashlib
import time
from django.shortcuts import render,HttpResponse
from django.conf import settings
from api.service import Handle
# redis/Memcache
api_key_record = {
    # "1b96b89695f52ec9de8292a5a7945e38|1501472467.4977243":1501472477.4977243
}
def decrypt(msg):
    from Crypto.Cipher import AES
    key = settings.DATA_KEY
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg) # result = b'\xe8\xa6\x81\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0sdfsd\t\t\t\t\t\t\t\t\t'
    data = result[0:-result[-1]]
    return str(data,encoding='utf-8')

def auto(func):
    def wrapper(request):
        client_md5_time_key = request.META.get('HTTP_OPENKEY')
        client_md5_key, client_ctime = client_md5_time_key.split('|')
        client_ctime = float(client_ctime)
        server_time = time.time()

        # 第一关
        if server_time - client_ctime > 10:
            return HttpResponse('【第一关】小伙子，别唬我，太长了')
        # 第二关
        temp = "%s|%s" % (settings.AUTH_KEY, client_ctime,)
        m = hashlib.md5()
        m.update(bytes(temp, encoding='utf-8'))
        server_md5_key = m.hexdigest()
        if server_md5_key != client_md5_key:
            return HttpResponse('【第二关】小子，你是不是修改时间了')

        for k in list(api_key_record.keys()):
            v = api_key_record[k]
            if server_time > v:
                del api_key_record[k]

        # 第三关:
        if client_md5_time_key in api_key_record:
            return HttpResponse('【第三关】有人已经来过了...')
        else:
            api_key_record[client_md5_time_key] = client_ctime + 10
        return func(request)
    return wrapper

@auto
def asset(request):
    if request.method == 'GET':
        ys = '重要的不能被闲杂人等看的数据'
        return HttpResponse(ys)

    # ########处理资产入库#############
    elif request.method == 'POST':
        # 新资产信息
        # print(decrypt(request.body))
        server_info = json.loads(decrypt(request.body))
        # print(server_info)
        obj = Handle(server_info)
        obj.handle()
        # for k,v in server_info.items():
        #     print(k,v)

        return HttpResponse('post成功')

    return HttpResponse('结束')

        # 资产表中以前资产信息
        # server_obj可以找到服务基本信息（单条）
        # disk_list = server_obj.disk.all()

        # 处理：
"""
1. 根据新资产和原资产进行比较：新["5","1"]      老["4","5","6"]
2. 增加: [1,]   更新：[5,]    删除：[4,6]
3. 增加：
        server_info中根据[1,],找到资产详细：入库
   删除：
        数据库中找当前服务器的硬盘：[4,6]

   更新：[5,]
        disk_list = [obj,obj,obj]

        {
            'data': {
                '5': {'slot': '5', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'},
                '3': {'slot': '3', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'},
                '4': {'slot': '4', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'},
                '0': {'slot': '0', 'capacity': '279.396', 'pd_type': 'SAS', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'},
                '2': {'slot': '2', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'},
                '1': {'slot': '1', 'capacity': '279.396', 'pd_type': 'SAS', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}
            },

            'status': True
        }

        log_list = []

        dict_info = {'slot': '5', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'},
        obj
            if obj.capacity != dict_info['capacity']:
                log_list.append('硬盘容量由%s变更为%s' %s(obj.capacity,dict_info['capacity'])
                obj.capacity = dict_info['capacity']
            ...
        obj.save()

        models.xxx.object.create(detail=''.join(log_list))

"""

            # 今天作业：(基本信息，硬盘，内存)
