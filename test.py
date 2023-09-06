# pip 源 -i https://pypi.tuna.tsinghua.edu.cn/simple
import requests
import re
# from urllib import parse
#
# # url编码相关
# data = '%CB%D1%CB%F7'
#
# print(parse.unquote(data,encoding="gbk"))

from lxml import etree
# headers = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#             'Accept-Language': 'zh-CN,zh;q=0.9',
#             'Cache-Control': 'no-cache',
#             'Connection': 'keep-alive',
#             'Pragma': 'no-cache',
#             'Referer': 'http://www.ranwen.me',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
#         }
# url = 'http://www.ranwen.me/modules/article/search.php?searchkey=%C4%E3%BA%C3&submit=%CB%D1%CB%F7&page=6'
# resp = requests.get(url=url,headers=headers)
# resp.encoding = "gbk"
# print(resp.text)
# pagesource = resp.text
# # root = etree.HTML(resp.text)
# # all_lst = root.xpath('/html/body/div[3]/table/tbody/tr[2]')
# # print(all_lst)
# obj = re.compile(r'<a href=.*?target="_blank" title=.*?>(?P<name>.*?)</a>.*?<td class="odd">(?P<author>.*?)'
#                  r'</td>.+?<td class="even">(?P<status>.*?)</td>',re.S)
# # name = obj.findall(pagesource)
# # name = re.findall(r'<a href=.*?target="_blank" title=.*?>(.*?)</a>',pagesource,re.S)
# result = obj.finditer(pagesource)
# for item in result:
#     name = item.group("name")
#     author = item.group("author")
#     status = item.group("status")
#     print(name,author,status)
# print()

# resp = requests.get(url="http://www.ranwen.me/book/12234/5452954.html",headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cache-Control': 'no-cache',
#     'Connection': 'keep-alive',
#     'Pragma': 'no-cache',
#     'Referer': 'http://www.ranwen.me/book/12234/',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
# })
# # print(resp.text)
#
# resp.encoding = "gbk"
# root = etree.HTML(resp.text)
# chapter_name = root.xpath('//*[@id="content"]/h1/text()')[0]
# content = "".join(root.xpath('//div[@id="htmlContent"]/text()')).replace(" 一秒记住【燃文小说网 www.ranwen.me】，精彩小说无弹窗免费阅读！","")
# print(chapter_name,content)
# with open("testt.html",mode="w",encoding="gbk") as f:
#     f.write(resp.text)