# - - coding:utf-8 - -
"""
# author: wktxzr
# Created Time : 20180408
# File Name: calculate_pd_main.py
# Description: 
计算当前话题下的p(q|d)，p（w|d），分别在不同query扩展下：
1、比赛时网页下TF-IDF扩展
2、比赛时新闻下TF-IDF扩展
3、维基百科下TF-IDF扩展
4、20180401网页下TF-IDF扩展（前50，前20）
5、20180401新闻下TF-IDF扩展（前50，前20）
"""

import os
import multiprocessing

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]
TOPICS = 'MB226 MB230 MB254 MB265 MB267 MB320 MB358 MB362 MB371 MB377 MB391 MB392 MB409 MB425'

def sys_order(topic):
	# parser.add_argument('-data', required = True, metavar = 'data', help = 'data file')
	# parser.add_argument('-topic', required = True, metavar = 'topic', help = 'which topic')
	# parser.add_argument('-output', required = True, metavar = 'output', help = 'output file')
	# parser.add_argument('-all_expand', required = True, metavar = 'expand file', help = 'expand file')
	# parser.add_argument('-k1', required = True, metavar = 'k1', help = 'bm25 k1')
	# parser.add_argument('-b', required = True, metavar = 'b', help = 'bm25 b')
	# parser.add_argument('-avg', required = True, metavar = 'avg', help = 'bm25 avg')
	data_path = CUR_PATH + '/init_data/'
	output_path = CUR_PATH + '/' + topic + '_data.txt'
	all_expand_path = CUR_PATH + '/src/all_expand.pkl'
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

