from repository import models

class Memory(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def func(self,server_info, server_obj):
        print('内存的操作')
        # new_memory_dict = {'DIMM #0': {'capacity': 1024, 'slot': 'DIMM #0', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'},
        #                    'DIMM #1': {'capacity': 0, 'slot': 'DIMM #1', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'},
        #                    'DIMM #2': {'capacity': 0, 'slot': 'DIMM #2', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'},
        #                    'DIMM #3': {'capacity': 0, 'slot': 'DIMM #3', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'},
        #                    'DIMM #4': {'capacity': 0, 'slot': 'DIMM #4', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'},
        #                    'DIMM #5': {'capacity': 0, 'slot': 'DIMM #5', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'},
        #                    'DIMM #6': {'capacity': 0, 'slot': 'DIMM #6', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'},
        #                    'DIMM #7': {'capacity': 0, 'slot': 'DIMM #7', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}}
        #采集到的内存信息
        new_memory_dict = server_info['memory']['data']
        #根据采集主机名查询到的主机所有内存
        old_memory_list = models.Memory.objects.filter(server_obj=server_obj)

        # 交集：5, 创建：3,删除4;
        new_slot_list = list(new_memory_dict.keys())
        #['DIMM #0','DIMM #1']
        old_slot_list = []
        for item in old_memory_list:
            old_slot_list.append(item.slot)

        # 交集：更新[5,]
        update_list = set(new_slot_list).intersection(old_slot_list)
        # 差集: 创建[3] 现在没有，采集到的有
        create_list = set(new_slot_list).difference(old_slot_list)
        # 差集: 删除[4] 现在有，新采集没有的
        del_list = set(old_slot_list).difference(new_slot_list)

        if del_list:
            # 删除
            models.Memory.objects.filter(server_obj=server_obj, slot__in=del_list).delete()
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除内存：%s" % ("、".join(del_list),))

        # 增加、
        record_list = []
        for slot in create_list:
            memory_dict = new_memory_dict[slot]
            # {'capacity': 1024, 'slot': 'DIMM #0', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}
            memory_dict['server_obj'] = server_obj
            models.Memory.objects.create(**memory_dict)
            temp = "新增内存:位置:{slot},容量:{capacity},型号:{model},频率:{speed},制造商:{manufacturer},SN号{sn}".format(**memory_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)

        # ############ 更新 ############
        record_list = []
        row_map = {'capacity': '容量', 'speed': '频率', 'model': '型号','manufacturer':'制造商','sn':'内存SN号'}
        for slot in update_list:
            new_memory_row = new_memory_dict[slot]
            ol_memory_row = models.Memory.objects.filter(slot=slot, server_obj=server_obj).first()
            for k, v in new_memory_row.items():
                # k: capacity;slot;pd_type;model
                # v: '476.939''xxies              DXM05B0Q''SATA'
                value = getattr(ol_memory_row, k)
                if v != value:
                    record_list.append("槽位%s,%s由%s变更为%s" % (slot, row_map[k], value, v,))
                    setattr(ol_memory_row, k, v)
            ol_memory_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)
        return
