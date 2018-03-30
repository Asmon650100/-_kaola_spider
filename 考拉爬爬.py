import json
import os

import re
import requests
import lxml.etree
#'===================================='
#=======================注意============================
# 页数
n=4
# 文件名
filename='考拉按摩机'

#====================================

for i in range(n):
    all_url="https://www.kaola.com/search.html?key=%25E6%258C%2589%25E6%2591%25A9%25E6%259C%25BA&pageNo="+str(i)+"&type=2"
    # Session保持绘话
    s = requests.Session()
    #请求头的搭建
    headers={
        'Referer': 'https://sundan.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    #抓取大的页面HTML
    all_html=s.get(all_url, headers=headers, verify=False).text
    # 获取连接
    my_tree = lxml.etree.HTML(all_html)
    li_list = my_tree.xpath("//*[@class=\"m-result\"]/ul/li/div/a/@href")  # 商品列表
    count=0
    # 爬之
    for li in li_list:
        temp_url = "https://www.kaola.com" + li  # 商品列表链接
        count += 1
        html = s.get(temp_url, headers=headers, verify=False).text
        my_tree = lxml.etree.HTML(html)

        #正则提取价格标题
        myrearch=re.findall( r"goods: (.*)\, \/\/商品信息",html,re.DOTALL)
        good_json=json.loads(myrearch[0])
        # 得到JSON
        print(good_json)
        #有些没有描述 防止程序OVER
        try:
            good_content=good_json['subTitle']
            print(good_content)
        except:
            good_content='该商品不存在描述'
            pass

        #拿价格
        good_price=good_json['suggestPrice']
        print(good_price)
        #标题
        good_title=good_json['title']
        print(good_title)
        # 拿图片
        img_list=good_json['goodsImageList']
        all_img_list=[]
        for i in range(len(img_list)):
            all_img_list.append(img_list[i]['imageUrl'])

        # 标题去掉空格，防止找不到文件路径
        title1 = ''.join(good_title.split(' '))
        if  '/' in title1:
            title1= ''.join(good_title.split('/'))
        if '/' in title1:
            title1 = ''.join(good_title.split('/'))
        if ' 'in title1:
            title1 = ''.join(good_title.split(' '))
        if os.path.exists("./考拉按摩机/" +title1 + "/"):
            continue
        else:
            os.makedirs("./考拉按摩机/" + title1 + "/")

        info='价格：'+str(good_price)+'\n'+'标题：'+good_title+'\n'+'描述：'+good_content
        with open("./考拉按摩机/" + title1 + "/info.txt", "w", encoding="utf-8") as mfile:
            mfile.write(info)

        for j in range(len(all_img_list)):
            with open("./考拉按摩机/"+ title1 + "/" + title1 + str(j) + ".jpg", "wb") as mfile_img:
                mfile_img.write(requests.get(all_img_list[j], verify=False).content)

