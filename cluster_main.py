# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20170503
# File Name: cluster_main.py
# Description: 聚类
"""
import os
import multiprocessing

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]
TOPICS = 'MB226 MB229 MB230 MB239 MB254 MB256 MB258 MB265 MB267 MB276 MB286 ' + \
'MB319 MB320 MB332 MB351 MB358 MB361 MB362 MB363 MB365 MB371 MB377 MB381 MB382 ' + \
'MB391 MB392 MB409 MB410 MB414 MB420 MB425 MB431 MB436 MB438 MB440 ' + \
'RTS1 RTS10 RTS13 RTS14 RTS19 RTS2 RTS21 RTS24 RTS25 RTS27 RTS28 RTS31 RTS32 RTS35 RTS36 RTS37 RTS4 RTS43 RTS5 RTS6'

def sys_order(topic, d, i):
	data_path = CUR_PATH + '/calculate_pqd/' + topic + '_data.txt'
	all_expand_path = CUR_PATH + '/src/web50_expand.pkl'
	word2vec_path = CUR_PATH + '/src/wiki.en.text.model'
	floder = CUR_PATH + '/d' + d + 'n' + str(i) + '/'
	output_tweet = floder + topic + '_' + d + '_' + str(i) + '_tweet.txt'
	if not os.path.exists(floder):
		os.makedirs(floder)

	order = 'python cluster.py' + ' -topic ' + topic + ' -data ' + data_path + \
	' -all_expand ' + all_expand_path +  ' -output_tweet ' + output_tweet + ' -n ' + d + \
	' -word2vec_path ' + word2vec_path
	print order
	os.system(order)


if __name__ == '__main__':
	d = '2'
	for i in xrange(2):
		pool = multiprocessing.Pool(processes = 3)
		topic_list = TOPICS.split(' ')
		for topic in topic_list:
			pool.apply_async(sys_order, args = (topic, d, i))
		pool.close()
		pool.join()
	d = '3'
	for i in xrange(2):
		pool = multiprocessing.Pool(processes = 3)
		topic_list = TOPICS.split(' ')
		for topic in topic_list:
			pool.apply_async(sys_order, args = (topic, d, i))
		pool.close()
		pool.join()
	d = '4'
	for i in xrange(2):
		pool = multiprocessing.Pool(processes = 3)
		topic_list = TOPICS.split(' ')
		for topic in topic_list:
			pool.apply_async(sys_order, args = (topic, d, i))
		pool.close()
		pool.join()
	d = '5'
	for i in xrange(2):
		pool = multiprocessing.Pool(processes = 3)
		topic_list = TOPICS.split(' ')
		for topic in topic_list:
			pool.apply_async(sys_order, args = (topic, d, i))
		pool.close()
		pool.join()
	d = '10'
	for i in xrange(2):
		pool = multiprocessing.Pool(processes = 3)
		topic_list = TOPICS.split(' ')
		for topic in topic_list:
			pool.apply_async(sys_order, args = (topic, d, i))
		pool.close()
		pool.join()
	# sys_order('MB226', '2', '0')
