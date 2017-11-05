# Create your views here.
# 定制分页类：
class PageInfo(object):
    def __init__(self, current_page, all_count, base_url,page_param_dict,per_page=10, show_page=11):
        """

                :param current_page:当前页
                :param all_count: 数据库总行数
                :param per_page: 每页显示行数
                :param base_url: 需要分页的url
                :param show_page: 页面可以显示的页数
                :return:
         """
        """将传入的当前页转为int 如果传入的为字符串，抛出异常直接
        将当前页设置为第一页"""
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1

        self.per_page = per_page
        """通过数据库所有数据的行数除以每页显示的行数，得到需要一共
        显示的页数，如果有余数则商要+1，余下的行单独一页"""
        a, b = divmod(all_count, per_page)
        if b:
            a = a + 1
        self.all_pager = a
        self.show_page = show_page
        self.base_url = base_url
        self.page_param_dict = page_param_dict

    """通过当前页码以及页面显示行数来获取页面上显示的具体行的数据
    如第1页就是1-10行，第2页为11-20行，"""

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page
    @property
    def end(self):
        return self.current_page * self.per_page

    """实际执行函数"""

    def pager(self):

        page_list = []
        # 如果页面上显示11页，样式应该是当前页前面一半后面一半，所以-1然后/2
        half = int((self.show_page - 1) / 2)
        # 如果数据总页数<11 show_page,即不足11页，就只显示数据一共能显示的页数
        if self.all_pager < self.show_page:
            begin = 1
            stop = self.all_pager
        # :param begin:当前页面显示的最左页，即第一页
        # :param stop: 当前显示的最右，即最后一页
        else:
            # 如果当前页 <=5,永远显示1,11
            if self.current_page <= half:
                begin = 1
                stop = self.show_page
            else:
                # 如果当前页+5 大于实际存在的最大页，比如一共有35页，当前页为
                # 32，再取后5页就是37，则36、37为空，所以加个判定，超过极限就
                # 取最右页为实际最大页，最左就是-11，即还是一共显示11页，
                if self.current_page + half > self.all_pager:
                    begin = self.all_pager - self.show_page + 1
                    stop = self.all_pager
                else:
                    # 这里为正常情况，显示当前页的前5页跟后5页
                    begin = self.current_page - half
                    stop = self.current_page + half

                    # 上一页功能
        # 当前页小于等于1，上一页没有内容
        if self.current_page <= 1:
            prev = "<li><a href='#'>上一页</a></li>"
        # 拼接字符串生成li a标签 上一页页数为当前页-1,添加到列表中
        else:
            self.page_param_dict['page'] = self.current_page - 1
            prev = "<li><a href='%s?%s'>上一页</a></li>" % (self.base_url, self.page_param_dict.urlencode(),)
        page_list.append(prev)

        # 当前页面同时显示的页面，由上面赋值的最左与最右页决定，+1是因为for循环range不顾尾
        for i in range(begin, stop + 1):
            self.page_param_dict['page'] = i
            if i == self.current_page:
                # 当前页给一个class，CSS显示效果区别于其它页
                temp = "<li class='active'><a  href='%s?%s'>%s</a></li>" % (self.base_url, self.page_param_dict.urlencode(), i,)
            else:
                temp = "<li><a href='%s?%s'>%s</a></li>" % (self.base_url, self.page_param_dict.urlencode(), i,)
            page_list.append(temp)

            # 下一页功能，同样的当前页>=最大页一样不跳转
        if self.current_page >= self.all_pager:
            nex = "<li><a href='#'>下一页</a></li>"
        else:
            self.page_param_dict['page'] = self.current_page + 1
            nex = "<li><a href='%s?%s'>下一页</a></li>" % (self.base_url, self.page_param_dict.urlencode(),)
        page_list.append(nex)
        # 此时列表中按顺序含有上一页的li a标签，需要显示的11页li a标签，以及下一页标签
        # 拼接成字符串并作为函数的返回值以供调用接收
        return ''.join(page_list)

