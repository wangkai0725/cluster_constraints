# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20180409
# File Name: nmf_main.py
# Description: 
"""

import os
import multiprocessing
import sys

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]
TOPICS = 'MB226 MB229 MB230 MB239 MB254 MB256 MB258 MB265 MB267 MB276 MB286 ' + \
'MB319 MB320 MB332 MB351 MB358 MB361 MB362 MB363 MB365 MB371 MB377 MB381 MB382 ' + \
'MB391 MB392 MB409 MB410 MB414 MB420 MB425 MB431 MB436 MB438 MB440 ' + \
'RTS1 RTS10 RTS13 RTS14 RTS19 RTS2 RTS21 RTS24 RTS25 RTS27 RTS28 RTS31 RTS32 RTS35 RTS36 RTS37 RTS4 RTS43 RTS5 RTS6'

if __name__ == '__main__':
	input_folder = sys.argv[1]
	output_folder = sys.argv[2]

	pool = multiprocessing.Pool(processes = 4)
	t_list = ['pqd', 'pqdqcall', 'pqded', 'pqdqcedall', 'pecall', 'pqdqcvi', 'pecvi', 'pqdqcedvi', 'ped']
	e = 'web50'
	for t in t_list:
		datas = os.listdir(input_folder)
		for data in datas:
			input_path = input_folder + '/' + data
			output_path = output_folder + '/' + e + '_' + t + '_' + data
			order = 'python rerank.py' + ' -type ' + t + ' -expand ' + e + \
				' -output_path ' + output_path + ' -input_path ' + input_path
			pool.apply_async(os.system, args = (order, ))
	pool.close()
	pool.join()

