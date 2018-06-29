# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20180628
# File Name: _main.py
# Description: 主函数

"""
import os

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]

# 目录，
# 760553618311352320*check hershey*20160802*1470136287.0*MB226*1*25.4*37.1*47.1*0.0*80.8*0.0
input_path = CUR_PATH + '/test/'
output_path = CUR_PATH + '/test_rerank/'

path_list = os.listdir(input_path)
for path in path_list:
	if not os.path.exists(output_path + '/' + path):
		os.makedirs(output_path + '/' + path)
	in1 = input_path + '/' + path
	out1 = output_path + '/' + path
	os.system('python rerank_main.py ' + in1 + ' ' + out1)
	os.system('python eval_main.py ' + out1 + ' > res.txt')
	os.system('python res_formal.py')
