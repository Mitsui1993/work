import copy
from types import FunctionType
from django.utils.safestring import mark_safe


class FilterOption(object):
    def __init__(self, field_or_func, is_multi=False, text_func_name=None, val_func_name=None):
        """
        :param field: 字段名称或函数
        :param is_multi: 是否支持多选
        :param text_func_name: 在Model中定义函数，显示文本名称，默认使用 str(对象)
        :param val_func_name:  在Model中定义函数，显示文本名称，默认使用 对象.pk
        """
        self.field_or_func = field_or_func
        self.is_multi = is_multi
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name

    @property
    def is_func(self):
        if isinstance(self.field_or_func, FunctionType):
            return True

    @property
    def name(self):
        if self.is_func:
            return self.field_or_func.__name__
        else:
            return self.field_or_func


class FilterList(object):

    def __init__(self,option,queryset,request):
        """

        :param option:
        :param queryset:
        :param request:
        """
        self.option = option
        self.queryset = queryset
        self.param_dict = copy.deepcopy(request.GET)
        self.path_info = request.path_info

    def __iter__(self):
        """
        对这个类的obj进行for循环会触发__iter__方法,
        拼接两个div ,左边为每一个option的“全部”标签，右边为字段筛选或函数筛选标签
        :return:
        """
        #“全部”开始
        yield mark_safe("<div class='all-area'>")
        if self.option.name in self.param_dict:
            #如果字段名或者函数名在筛选字典里，表示已经点过其中至少一个，
            #把包含此字段从param_dict中移除，先获取点击全部的url，再将它设置回去
            pop_val = self.param_dict.pop(self.option.name)
            url = "{0}?{1}".format(self.path_info,self.param_dict.urlencode())
            self.param_dict.setlist(self.option.name,pop_val)
            yield mark_safe("<a href='{0}'>全部</a>".format(url))
        else:
            #如果字段不在筛选里，说明此时点击的已经是全部，直接拼接url并设置active属性
            url = "{0}?{1}".format(self.path_info, self.param_dict.urlencode())
            yield mark_safe("<a class='active' href='{0}'>全部</a>".format(url))
        #“全部”div拼接完成，开始右半部分单个筛选的div
        yield mark_safe("</div><div class='others-area'>")

        for row in self.queryset:
            """row为此字段对应的每一行数据"""
            #当多次点击同一个筛选条件时，param_dict会不停的append同一个条件，
            #因此需要每次进入循环时，重新获取一次真实的param_dict
            param_dict = copy.deepcopy(self.param_dict)
            #当self.option.val_func_nam或test_func...为真，说明为函数，需要在model类里面自定义这个函数，
            #通过getattr 并加括号运行即可拿到字段的返回值，如果未设置默认拿pk与类的__str__返回值
            val = str(getattr(row,self.option.val_func_name)() if self.option.val_func_name else row.pk)
            text = getattr(row,self.option.text_func_name)() if self.option.text_func_name else str(row)
            active = False
            if self.option.is_multi:
                #如果是PK或者M2M字段
                value_list = param_dict.getlist(self.option.name)
                if val in value_list:
                    """如url GET请求中已经有这个选项，则a标签应当将这个选项移除选中状态,
                    并设置active属性"""
                    value_list.remove(val)
                    active = True
                else:
                    #request.GET的append方法
                    param_dict.appendlist(self.option.name,val)

            else:
                value_list = param_dict.getlist(self.option.name)
                if val in value_list:
                    active = True
                param_dict[self.option.name] = val

            url = "{0}?{1}".format(self.path_info,param_dict.urlencode())
            if active:
                tpl = "<a class='active' href='{0}'>{1}</a>".format(url,text)
            else:
                tpl = "<a href='{0}'>{1}</a>".format(url, text)
            yield mark_safe(tpl)

        yield mark_safe("</div>")