#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123', db='autopage',charset='utf8')
cur = conn.cursor()


# channellist = ['drive','news','advice']
# channellist = ['drive']

channel_dict = {'drive': '试驾评测', 'news': '新闻', 'advice': '导购'}

for channel, value in channel_dict.items():

    for page in range(1, 2):
        try:
            start_url = "http://www.autohome.com.cn/%s/%s/#liststart" % (channel, page,)
            html = requests.get(start_url)
            soup = BeautifulSoup(html.text, 'html.parser')

            dest_posite = soup.find(id="auto-channel-lazyload-article")

            li_postie = soup.find_all("li")

            for i in li_postie:
                url_tag = i.find("a")
                if not url_tag:
                    continue
                url = url_tag.attrs['href']

                title_tag = i.find("h3")
                if not title_tag:
                    continue
                title = title_tag.get_text()

                summary_tag = i.find("p")
                if not summary_tag:
                    continue
                summary = summary_tag.get_text()
                # ##################  ##################

                # 判断详细页面是否有分页
                has_sub_pager = BeautifulSoup(requests.get(url).text, 'html.parser')
                if has_sub_pager.find(class_='page'):
                    url_part_list = url.rsplit('.', 1)
                    url = "%s-all.%s" % (url_part_list[0], url_part_list[1],)

                # ########### 新添加代码开始：url是否已经存在，如果已经存在，则不在继续爬取 ###########
                cur.execute('select count(1) from art_main where url=%s', (url,))
                if cur.fetchone()[0]:
                    continue
                # ########### 新添加代码结束：url是否已经存在，如果已经存在，则不在继续爬取 ###########

                # 获取详细页面信息
                detail = requests.get(url)
                detail_soup = BeautifulSoup(detail.text, 'html.parser')
                # 详细页面：创建时间
                ctime_tag = detail_soup.find(id='articlewrap')
                if not ctime_tag:
                    continue
                ctime = ctime_tag.find(class_='article-info').find('span').get_text()
                # 详细页面：来源
                art_source = detail_soup.find(id='articlewrap').find(class_='article-info').find_all('span')[1].get_text()
                # 详细页面：类型
                article_type = detail_soup.find(id='articlewrap').find(class_='article-info').find_all('span')[2].get_text()

                # 向主表中插入一行数据：在数据库中插入数据，并获取自增ID
                sql = 'insert into art_main(title,summary,ctime,status,art_source,art_type,url) values(%s,%s,%s,%s,%s,%s,%s)'
                cur.execute(sql, (title, summary, ctime, 0, art_source, value, url))
                # 获取心插入数据行的自增ID
                new_main_id = cur.lastrowid

                count = 0
                content = detail_soup.find(id='articleContent')
                sub_sql = "insert into art_sub(main_id,note_index,content) values(%s,%s,%s)"
                # 获取详细页面的每一块：
                # 将每一块都插入到子表中
                for tag in content.find_all(recursive=False):
                    count += 1
                    if tag.name == 'table':
                        text = tag.encode()
                        cur.execute(sub_sql, (new_main_id, count, text))
                    elif tag.find('table'):
                        text = tag.find('table').encode()
                        cur.execute(sub_sql, (new_main_id, count, text))
                    elif tag.find_all('img'):
                        for img_tag in tag.find_all('img'):
                            text = img_tag.attrs.get('src')  # 获取图片的URL
                            cur.execute(sub_sql, (new_main_id, count, text))
                            # 在详细表中插入一条数据
                    else:
                        text = tag.get_text()
                        cur.execute(sub_sql, (new_main_id, count, text))
                conn.commit()
        except Exception as e:
            print(e)
cur.close()
conn.close()