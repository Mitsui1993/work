from repository import models
from django.shortcuts import render,HttpResponse
from django.conf import settings
import importlib

class Handle(object):
    def __init__(self,server_info):
        self.server_info = server_info
        self.hostname = self.server_info['basic']['data']['hostname']
        self.server_obj = models.Server.objects.filter(hostname=self.hostname).first()

    #异常情况函数，如主机未录入以及资产信息出错
    def foo(self):
        # print('主逻辑操作')
        if not self.server_obj:
            return HttpResponse('当前主机名在资产中未录入')

        e_msg = {"basic":"基本数据","board":"主板","cpu": "处理器","disk":"硬盘","memory":"内存","nic":"网卡"}
        error_list = []
        for k,v in self.server_info.items():
            #错误时，写入错误信息
            if not v['status']:
                error_list.append(k)
                models.ErrorLog.objects.create(content=self.server_info[k]['data'], asset_obj=self.server_obj.asset,
                                               title='【%s】%s采集错误信息' % (self.hostname,e_msg[k]))

        return error_list

    #正常情况，采集正确时，进行数据更新
    def handle(self):
        error_list = self.foo()
        for k,v in settings.PLUGINS_DICT.items():
            if k in error_list:
                continue
            module_path, class_name = v.rsplit('.', 1)
            m = importlib.import_module(module_path)
            cls = getattr(m, class_name)
            if hasattr(cls, 'initial'):
                obj = cls.initial()
            else:
                obj = cls()
            obj.func(self.server_info,self.server_obj)

