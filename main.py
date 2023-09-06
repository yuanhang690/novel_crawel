import time
from multiprocessing.dummy import Pool
from urllib import parse
from lxml import etree
import requests
import re
import os


class Ranwen:

    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'http://www.ranwen.me',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        # 用于存储书籍信息
        self.datas = []
        self.url = 'http://www.ranwen.me/'

    def run(self):
        """
        搜索想要看的小说
        :return:
        """
        # 要查找的
        search_name = input("请输入你要查找的小说:")
        info = parse.quote(search_name,encoding="gbk")
        search_url = f'http://www.ranwen.me/modules/article/search.php?searchkey={info}&submit=%CB%D1%CB%F7&page=1'
        self.resp = requests.get(url=search_url,headers=self.headers)
        self.resp.encoding = "gbk"
        # 获取搜索的结果有几页
        page_index = int(re.search('class="last">(?P<index>\d+)</a>',self.resp.text).group("index"))
        # print(page_index)

        for i in range(1,page_index+1):
            search_url = f"http://www.ranwen.me/modules/article/search.php?searchkey={info}&submit=%CB%D1%CB%F7&page={i}"
            self.resp = requests.get(url=search_url, headers=self.headers)
            self.resp.encoding = "gbk"
            # 解析当前页数
            self.parse_source(self.resp.text)
        # print(resp.text)
        # book_lst =

    def parse_source(self,resp_text):
        """
        获取搜索的结果
        :param resp_text: 页面信息
        :return:
        """
        print("请稍等。。。")
        obj = re.compile(
            r'<td class="odd"><a href="(?P<link>.*?)" target="_blank" title=.*?>(?P<name>.*?)</a>.*?<td class="odd">(?P<author>.*?)'
            r'</td>.+?<td class="even">(?P<status>.*?)</td>',
            re.S,
        )
        result = obj.finditer(resp_text)
        # print("书名\t作者\t连载状况")
        for item in result:
            data = {
                "book_name": item.group("name"),
                "author": item.group("author"),
                "status": item.group("status"),
                "link": item.group("link")
            }
            self.datas.append(data)

        # print(self.datas)
        self.select_book()

    def select_book(self):
        """
        选择想要下载的书本
        :return:None
        """
        for index,book in enumerate(self.datas):
            print(index,f"书名:{book['book_name']}\t",f'作者:{book["author"]}\t',f'状态:{book["status"]}')

        select = int(input("请输入要下载的小说序号:"))
        self.parse_book_info(select)


    def parse_book_info(self,select):
        # 获取名字，链接
        book_url = self.datas[select]["link"]
        name = self.datas[select]["book_name"]

        print(book_url)
        # 1.获取小说目录地页数：
        catalogue_resp = requests.get(url=book_url,headers=self.headers)
        try:
            page = int(re.search('<option value=.*?>第(?P<page>\d+)页\(末页\)</option>',catalogue_resp.text,re.S).group("page"))
        except:
            page = 1

        # 2.获取每个章节的url
        url = ""
        # 存储每个章节的url
        self.link_list = []
        for i in range(1,page+1):
            print(f"正在解析第{i}页目录,请稍等")
            url = book_url + f'index_{i}.html'
            chapter_source = requests.get(url=url,headers= {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': f'http://www.ranwen.me/book/3068/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
})
            root = etree.HTML(chapter_source.text)
            li_list = root.xpath('/html/body/div[4]/div/ul[@class="mulu_list"]/li')
            for li in li_list:


                # a = li.xpath("./a/@href")
                # print(a)
                # 过滤第一个没信息的
                try:
                    chapter_url = book_url + li.xpath('./a/@href')[0]
                except Exception as e:
                    print("页数：",i)
                    print(e)
                    continue
                # print(chapter_url)
                # 将每一个目录的链接加入link_ist中
                self.link_list.append(chapter_url)
            time.sleep(0.5)
        print("准备创建目录")
        if not os.path.exists(f'./{name}'):
            os.mkdir(f'./{name}')
        # 准备多线程
        threading_pool = Pool(30)
        # 获取总长度
        book_length = len(self.link_list)
        for index,item in enumerate(self.link_list):
            # 如果该章节不在目录，说明没下载过（避免因特殊问题下到一半终止，导致需要完全重新开始下载）
            if f'{index}.txt' not in os.listdir(f'./{name}'):
                threading_pool.apply_async(self.download_one,args=(name,index,item,))
        threading_pool.close()
        threading_pool.join()
        print('下载完成')
        self.merge_book(name,book_length)


    def download_one(self,name,index,link):
        """
        多线程的下载任务target
        :param name: 书名
        :param index: 章节
        :param link: 详情页
        :return:
        """
        print(f"下载第{index}个")

        for i in range(5):
            # 爬虫的自省
            try:
                #发送请求并解析数据
                resp = requests.get(url=link,headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'http://www.ranwen.me/book/12234/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        })
                root = etree.HTML(resp.text)
                chapter_name = root.xpath('//*[@id="content"]/h1/text()')[0]
                content = "".join(root.xpath('//div[@id="htmlContent"]/text()')).replace(" 一秒记住【燃文小说网 www.ranwen.me】，精彩小说无弹窗免费阅读！","")
                print(chapter_name)
                with open(f'./{name}/{index}.txt',mode="w",encoding="utf-8") as f:
                    f.write(chapter_name)
                    f.write(content)
                    print("保存完成")

                break
            except Exception as e:
                print(e,'准备重试')
                time.sleep(1)

    def merge_book(self,book_name,book_length):
        """
        合并下载后的内容
        :param book_name:
        :return:
        """
        print("准备合并")
        # 切换工作目录
        # 1.记录当前工作目录
        now_dir = os.getcwd()
        # 2.切换
        os.chdir(f"./{book_name}")

        # 进行合并
        # 命令：copy /b a.txt + b.txt + c.txt xxx.txt
        if book_length<100:
            temp = []
            for i in range(book_length):
                temp.append(f'{i}.txt')
            names = " + ".join(temp)
            os.system(f"copy /b {names} {book_name}.txt")
        else:
            #每100个合并一次
            temp = []
            n = 1
            for i in range(book_length):
                temp.append(f'{i}.txt')
                if i!=0 and i%100==0:
                    names =" + ".join(temp)
                    os.system(f"copy /b {names} 合{n}.txt")
                    n +=1
                    temp = []
            # 把最后未合并的进行收尾
            names = " + ".join(temp)
            os.system(f"copy /b {names} 合{n}.txt")

            # 把所有的n进行循环
            # 第二次合并
            temp2 = []
            for i in range(1,n+1):
                temp2.append(f"合{i}.txt")
            names2 = " + ".join(temp2)
            os.system(f"copy /b {names2} {book_name}.txt")




        # 3.完事后要换回来
        os.chdir(now_dir)
        print("合并完成")








if __name__ == '__main__':
    ranwen = Ranwen()
    ranwen.run()
