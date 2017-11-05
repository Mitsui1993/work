from repository import models

class Nic(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def func(self,server_info, server_obj):
        print('网卡操作')
        """
        {'eth0': {'up': True, 'hwaddr': '00:1c:42:a5:57:7a', 'ipaddrs': '10.211.55.4', 'netmask': '255.255.255.0'}}"""
        new_nic_dict = server_info['nic']['data']
        # 根据采集主机名查询到的主机所有网卡
        old_nic_list = models.NIC.objects.filter(server_obj=server_obj)

        # 交集：5, 创建：3,删除4;
        new_name_list = list(new_nic_dict.keys())
        # ['DIMM #0','DIMM #1']
        old_name_list = []
        for item in old_nic_list:
            old_name_list.append(item.name)

        print(new_name_list,old_name_list)
        # 交集：更新[eth0,]
        update_list = set(new_name_list).intersection(old_name_list)
        # 差集: 创建[3] 现在没有，采集到的有
        create_list = set(new_name_list).difference(old_name_list)
        # 差集: 删除[4] 现在有，新采集没有的
        del_list = set(old_name_list).difference(new_name_list)

        if del_list:
            # 删除
            models.Memory.objects.filter(server_obj=server_obj, name__in=del_list).delete()
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除网卡：%s" % ("、".join(del_list),))

        # 增加、
        record_list = []
        for name in create_list:
            nic_dict = new_nic_dict[name]
            # {'capacity': 1024, 'slot': 'DIMM #0', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}
            nic_dict['server_obj'] = server_obj
            nic_dict['name'] = name
            models.NIC.objects.create(**nic_dict)
            temp = "新增网卡:名称:{name},MAC地址:{hwaddr},ip地址:{ipaddrs},子网掩码:{netmask}".format(**nic_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

        # ############ 更新 ############
        record_list = []
        row_map = {'name': '名称', 'hwaddr': 'MAC地址', 'ipaddrs': 'ip地址', 'netmask': '子网掩码', 'sn': '内存SN号','up':'状态'}
        for name in update_list:
            new_nic_row = new_nic_dict[name]
            ol_nic_row = models.NIC.objects.filter(name=name, server_obj=server_obj).first()
            for k, v in new_nic_row.items():
                # k: capacity;slot;pd_type;model
                # v: '476.939''xxies              DXM05B0Q''SATA'
                value = getattr(ol_nic_row, k)
                if v != value:
                    record_list.append("网卡%s,%s由%s变更为%s" % (name, row_map[k], value, v,))
                    setattr(ol_nic_row, k, v)
            ol_nic_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)
        return