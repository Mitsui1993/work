from django.template import Library
from types import FunctionType

register = Library()

def table_body(result_list,list_display,admin_obj):
    """
    循环自定制的列表，生成对应的标签数据
    :param result_list: 数据表所有数据
    :param list_display: 自定制列表  ['id','name',fun]
    :param admin_obj: 继承自BaseAdmin的models类对象，如:AdminUserInfo()
    :return:
    """
    for row in result_list:
        if list_display == "__all__":
            yield [str(row)]
        else:
            yield [name(admin_obj,row) if isinstance(name,FunctionType) else getattr(row,name) for name in list_display]

def table_header(list_display,admin_obj):
    """
    表头名称显示
    :param list_display:
    :param admin_obj:
    :return:
    """
    if list_display == "__all__":
        yield "对象列表"
    else:
        for item in list_display:
            if isinstance(item,FunctionType):
                #是函数，显示定制的中文
                yield item(admin_obj,is_header = True)
            else:
                #不是函数，显示字段的verbose_name值
                #get_field(username) = models.Charfiled()对象，可以有verbose_name属性
                yield admin_obj.model_class._meta.get_field(item).verbose_name

@register.inclusion_tag("md/md.html")
def func(result_list,list_dispaly,admin_obj):
    """
    inclusion_tag，调用这个tag的模版，首先会将数据交给md.html根据html渲染出标签，
    然后替换到调用这个tag的位置。
    :param result_list:
    :param list_dispaly:
    :param admin_obj:
    :return:
    """
    v = table_body(result_list,list_dispaly,admin_obj)
    h = table_header(list_dispaly,admin_obj)

    return {'res':v,'hd_list':h}