from repository import models

class Cpu(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def func(self,server_info, server_obj):
        print('CPU操作')
        new_cpu_dict = server_info['cpu']['data']
        """
        {'cpu_count': 24, 'cpu_physical_count': 2, 'cpu_model': ' Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz'}"""
        record_list = []
        row_map = {'cpu_count': 'CPU个数', 'cpu_physical_count': 'CPU物理个数','cpu_model':'CPU型号'}
        for k, v in new_cpu_dict.items():
            value = getattr(server_obj, k)
            if v != value:
                record_list.append("CPU变更：%s由%s变更为%s" % (row_map[k], value, v,))
                setattr(server_obj, k, v)
        server_obj.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)
        return