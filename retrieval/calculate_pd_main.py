# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20180508
# File Name: calculate_pd_main.py
# Description: 
计算当前话题下的P(Q|D)，P(E|D)
Q表示10个词的主题扩展
E表示全部扩展词的主题扩展
D表示推特
"""

import os
import multiprocessing

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]
TOPICS = 'MB226 MB230 MB254 MB265 MB267 MB320 MB358 MB362 MB371 MB377 MB391 MB392 MB409 MB425'

def sys_order(topic):
	# 预处理后的推特数据
	data_path = CUR_PATH + '/init_data/'
	output_path = CUR_PATH + '/' + topic + '_data.txt'
	# 扩展后的主题
	# 对比了几种不同的扩展方式，所以多一层key
	# all_expand['wiki'] = wiki_expand 
	# wiki_expand[topic] = [(q,tf,idf)]
	all_expand_path = CUR_PATH + '/src/all_expand.pkl'
	# BM25经验常量
	k1 = '2'
	b = '0.75'
	avg = '19'
	
	order = 'python calculate_pd.py' + ' -topic ' + topic + ' -data ' + data_path + \
	' -all_expand ' + all_expand_path +  ' -k1 ' + k1 + ' -b ' + b + ' -avg ' + avg +  ' -output ' + output_path
	print order
	os.system(order)


if __name__ == '__main__':
	pool = multiprocessing.Pool(processes = 14)
	topic_list = TOPICS.split(' ')
	for topic in topic_list:
		pool.apply_async(sys_order, args = (topic, ))
	pool.close()
	pool.join()

