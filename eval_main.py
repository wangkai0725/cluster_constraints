# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20180628
# File Name: eval_main.py
# Description: 
"""

import os
import sys

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]
TOPICS = 'MB226 MB229 MB230 MB239 MB254 MB256 MB258 MB265 MB267 MB276 MB286 ' + \
'MB319 MB320 MB332 MB351 MB358 MB361 MB362 MB363 MB365 MB371 MB377 MB381 MB382 ' + \
'MB391 MB392 MB409 MB410 MB414 MB420 MB425 MB431 MB436 MB438 MB440 ' + \
'RTS1 RTS10 RTS13 RTS14 RTS19 RTS2 RTS21 RTS24 RTS25 RTS27 RTS28 RTS31 RTS32 RTS35 RTS36 RTS37 RTS4 RTS43 RTS5 RTS6'

if __name__ == '__main__':
	src_path = CUR_PATH + '/src/'
	q = src_path + '/qrels.txt'
	c = src_path + '/rts2016-batch-clusters.json'
	t = src_path + '/rts2016-batch-tweets2dayepoch.txt'
	
	data_path = sys.argv[1]
	# data_path = CUR_PATH + '/wtf/'
	runs = os.listdir(data_path)
	for run in runs:
		data = data_path + '/' + run
		topic = run.split('_')[2]
		order = 'python eval.py' + ' -q ' + q + ' -c ' + c + ' -t ' + t + ' -r ' + data +  ' -m ' + topic
		os.system(order)

