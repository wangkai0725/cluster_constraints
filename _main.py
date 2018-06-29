# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20180628
# File Name: _main.py
# Description: 主函数
包括
微博重排序
结果评测
输出结果
"""
import os

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]

# 聚类后的微博文本总目录
# 底层每次实验单独列出一个目录
input_path = CUR_PATH + '/test/'
# 输出目录
output_path = CUR_PATH + '/test_rerank/'

path_list = os.listdir(input_path)
for path in path_list:
	if not os.path.exists(output_path + '/' + path):
		os.makedirs(output_path + '/' + path)
	in1 = input_path + '/' + path
	out1 = output_path + '/' + path
	# 重排序
	os.system('python rerank_main.py ' + in1 + ' ' + out1)
	# 评测
	os.system('python eval_main.py ' + out1 + ' > res.txt')
	# 输出结果
	os.system('python res_formal.py')
