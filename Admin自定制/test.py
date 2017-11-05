class FilterList(object):

    def __init__(self,option,data_list):
        self.option = option
        self.data_list = data_list

    def show(self):
        self.option.nick()

    def __iter__(self):
        yield "全部："
        for i in self.data_list:
            yield "<a href='{0}'>{1}</a>".format(i,self.option.bs+i)


class FilterOption(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def nick(self):
        tpl = self.name + str(self.age)
        return tpl

    @property
    def bs(self):
        if self.age > 15:
            return "喜欢"
        else:
            return "讨厌"

#对象封装另一个类的对象，可以调用另一个对象的方法
#每个对象划分职责：操作自己的参数
obj_list = [
    FilterList(FilterOption("刘德华",18),["参选特首","唱歌","拍戏"]),
    FilterList(FilterOption("张学友",20),["做表情","唱歌","拍戏","讲笑话"]),
    FilterList(FilterOption("黎明",13),["凹造型","唱歌",]),
    FilterList(FilterOption("郭富城",18),["跳舞","唱歌","拍戏"]),
]

for obj in obj_list:
    for item in obj:
        print(item,end="  ")
    else:
        print('')


















