# -*-coding:utf-8-*-
"""
# author: wktxzr
# Created Time : 20180412
# File Name: spider.py
# Description: 
获取维基百科内容
"""
import json
import wikipedia
import pickle

with open('TREC2016-RTS-topics.json') as inputfile:
	topic1 = json.load(inputfile)
with open('TREC2015-MB-noeval-topics-culled.json') as inputfile:
	topic2 = json.load(inputfile)

TOPICS = 'MB226 MB229 MB230 MB239 MB254 MB256 MB258 MB265 MB267 MB276 MB286 ' + \
'MB319 MB320 MB332 MB351 MB358 MB361 MB362 MB363 MB365 MB371 MB377 MB381 MB382 ' + \
'MB391 MB392 MB409 MB410 MB414 MB420 MB425 MB431 MB436 MB438 MB440 ' + \
'RTS1 RTS10 RTS13 RTS14 RTS19 RTS2 RTS21 RTS24 RTS25 RTS27 RTS28 RTS31 RTS32 RTS35 RTS36 RTS37 RTS4 RTS43 RTS5 RTS6'

topic_list = TOPICS.split(' ')
new_list = []
new_dic = {}

topic = topic1 + topic2
for t in topic:
	if t['topid'] not in topic_list:
		continue
	print t['topid']
	try:
		summary = wikipedia.summary(t['description'])
	except:
		summary = '-'
	finally:
		print summary
		if summary != '-':
			new_list.append(t['topid'])
			new_dic[t['topid']] = summary


with open('wiki.pkl', 'wb') as outputfile:
	pickle.dump(new_dic, outputfile)

print new_list
print len(new_list)
print len(topic_list)

