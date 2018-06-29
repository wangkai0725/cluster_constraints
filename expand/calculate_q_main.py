# - - coding:utf-8 - -
"""
# author: wktxzr
# Created Time : 20180503
# File Name: calculate_q_main.py
# Description: 
计算IDF
"""

import os
import multiprocessing

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]
TOPICS = 'MB226 MB230 MB254 MB265 MB267 MB320 MB358 MB362 MB371 MB377 MB391 MB392 MB409 MB425'

def sys_order(topic):
	# 预处理后的推特数据
	data_path = CUR_PATH + '/init_data/'
	# 扩展词
	# dic[topic] = word_list
	topic_day_path = CUR_PATH + '/id_newsexword_dic_20.pkl'
	
	output_path = CUR_PATH + '/' + topic + '.pkl'
	
	order = 'python calculate_q.py' + ' -d ' + data_path + ' -o ' + \
	output_path + ' -i ' + topic_day_path +  ' -w ' + topic + ' -k ' + \
	k1 +  ' -b ' + b +  ' -v ' + avgdl
	os.system(order)

if __name__ == '__main__':
	pool = multiprocessing.Pool(processes = 7)
	topic_list = TOPICS.split(' ')
	for topic in topic_list:
		pool.apply_async(sys_order, args = (topic, ))
	pool.close()
	pool.join()
	# topic_list = TOPICS.split(' ')
	# for topic in topic_list:
	# 	sys_order(topic)