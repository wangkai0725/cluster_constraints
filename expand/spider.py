# -*-coding:utf-8-*-
"""
# author: wktxzr
# Created Time : 20180412
# File Name: spider.py
# Description: 
谷歌镜像网站爬虫，镜像网站的格式基本都一样，以后还是用beautifulsoup更方便
"""

import requests
import random
import pickle
from lxml import etree
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 给定主题编号
TOPICS = 'MB229 MB239 MB256 MB258 MB276 MB286 MB319 MB332 MB351 MB361 MB363 ' + \
'MB365 MB381 MB382 MB410 MB414 MB420 MB431 MB436 MB438 MB440 RTS1 RTS10 RTS13 RTS14 '+ \
'RTS19 RTS2 RTS21 RTS24 RTS25 RTS27 RTS28 RTS31 RTS32 RTS35 RTS36 RTS37 RTS4 RTS43 RTS5 RTS6'

topic_list = TOPICS.split(' ')
# 字典格式
# dic['MB229'] = title
with open('id_title_dic.pkl') as inputfile:
	title_dic = pickle.load(inputfile)

dic = {}
for topic in topic_list:
	query = title_dic[topic]
	# num 每页条数
    # lang=en 英文结果
    # tbm=nws 新闻结果
	url='https://google.gccpw.cn/search?num=20&site=&source=lnms&q=%s&lang=en&tbm=nws&sa=X' %query

	headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'en-us;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }

	proxy = [
	"http://49.128.162.55:8080",
	"http://164.132.11.206:3128",
	"http://121.149.232.110:3129",
	"http://104.131.26.132:80",
	"http://86.102.32.88:8080",
	"http://108.61.167.117:8080",
	"http://94.141.179.58:3128",
	"http://187.49.30.106:8088",
	"http://219.112.217.237:8080",
	"http://5.148.97.35:3128"]

	mysession = requests.Session()
	mysession.verify = False
	mysession.headers = headers
	mysession.proxy = random.choice(proxy)

	try:
		req = mysession.get(url)
	except:
		req = mysession.get(url)
	sleep(random.randint(1,20)*1)
	while req.status_code != 200:
		mysession.proxy = random.choice(proxy)
		req = mysession.get(url)
		sleep(random.randint(1,20)*1)

	page = etree.HTML(req.text)

	res_list = []
	# 检索结果总标签，每个镜像网站格式一样，具体标签不同
	result = page.xpath(u'//div[@class="gG0TJc"]')
	for res in result:
		# 结果标题
		title = res.xpath(u'descendant::h3[@class="r dO0Ag"]')
		if(len(title) != 0):
			title_text = " ".join(title[0].xpath("descendant-or-self::text()"))
		else:
			title_text = 'none'
		# 结果描述
		describe = res.xpath(u'descendant::div[@class="st"]')
		if(len(describe) != 0):
			describe_text = " ".join(describe[0].xpath("descendant-or-self::text()"))
		else:
			describe_text = 'none'
		res_list.append([title_text, describe_text])

	# 存为字典格式，不区分段落
	# dic[topic] = describe
	value = ''
	for r in res_list:
		value += r[0]
		value += ' '
		value += r[1]
		value += ' '
	dic[topic] = value
	print topic
	print query
	print dic[topic]

with open('id_news_dic_20.pkl', 'wb') as outputfile:
	pickle.dump(dic, outputfile)
