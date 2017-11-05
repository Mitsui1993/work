from repository import models

class Basic(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def func(self,server_info, server_obj):
        new_basic_dict = server_info['basic']['data']
        """
        {"os_platform": "linux", "os_version": "CentOS release 6.6 (Final)\\nKernel \\r on an \\\\m", "hostname": "c2.com"}"""
        record_list = []
        row_map = {'os_platform': '操作系统', 'os_version': '系统版本'}
        for k, v in new_basic_dict.items():
            value = getattr(server_obj, k)
            if v != value:
                record_list.append("主机变更：%s由%s变更为%s" % (row_map[k], value, v,))
                setattr(server_obj, k, v)
        server_obj.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)
        return

