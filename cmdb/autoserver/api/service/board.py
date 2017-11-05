from repository import models

class Board(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def func(self,server_info, server_obj):
        print('主板操作')
        new_board_dict = server_info['board']['data']
        """
        {'manufacturer': 'Parallels Software International Inc.', 'model': 'Parallels Virtual Platform',
        'sn': 'Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30'}"""
        record_list = []
        row_map = {'manufacturer': '制造商', 'model': '型号','sn':'SN号'}
        for k, v in new_board_dict.items():
            value = getattr(server_obj, k)
            if v != value:
                record_list.append("主板变更：%s由%s变更为%s" % (row_map[k], value, v,))
                setattr(server_obj, k, v)
        server_obj.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)
        return