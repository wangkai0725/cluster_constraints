# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20180508
# File Name: calculate_pd.py
# Description:
计算当前话题下的P(Q|D)，P(E|D)
Q表示10个词的主题扩展
E表示全部扩展词的主题扩展
D表示推特
"""
import sys
import time
import math
import os
import pickle
import argparse
from itertools import groupby
reload(sys)
sys.setdefaultencoding('utf-8')
TYPE_DIC = {'wiki':0, 'oldn':1, 'oldw':2, 'news50':3, 'web50':4, 'news20':5, 'web20':6}

class Tweet(object):
	def __init__(self, topic):
		self.tweet_id = ''
		self.tweet_word_list = []
		self.tweet_day = ''
		self.tweet_time = ''
		self.tweet_topic = topic
		self.tweet_pqd = [0.0] * 7
		self.tweet_ped = [0.0] * 7


	def load(self, line):
		l = line.strip().split('*')
		# topic*760264030984347648*mood*Tue Aug 02 00:00:44 +0000 2016
		self.tweet_id = l[1]
		self.tweet_word_list = l[2].split(' ')
		dt = l[3].strip().split(' ')
		self.tweet_day = '201608' + dt[2]
		fdt = '201608' + dt[2] + ' ' + dt[3]
		timeArray = time.strptime(fdt, "%Y%m%d %H:%M:%S")
		#转换成时间数组
		timestamp = time.mktime(timeArray)
		#转换成时间戳
		self.tweet_time = timestamp


	def set_topic(self, topic):
		self.tweet_topic = topic


	def get_topic(self):
		return self.tweet_topic


	def get_id(self):
		return self.tweet_id


	def get_word_list(self):
		return self.tweet_word_list


	def get_time(self):
		return self.tweet_time


	def get_day(self):
		return self.tweet_day


	def set_tweet_pqd(self, pqd, expand_type_index):
		self.tweet_pqd[expand_type_index] = pqd


	def get_tweet_pqd(self, expand_type_index):
		return self.tweet_pqd[expand_type_index]

	def get_tweet_sumpqd(self):
		return sum(self.tweet_pqd)


	def set_tweet_ped(self, ped, expand_type_index):
		self.tweet_ped[expand_type_index] = ped


	def get_tweet_ped(self, expand_type_index):
		return self.tweet_ped[expand_type_index]


	def print_tweet(self):
		return '*'.join([self.tweet_id, ' '.join(self.tweet_word_list), self.tweet_day, str(self.tweet_time), self.tweet_topic, \
			' '.join([str(i) for i in self.tweet_pqd]), ' '.join([str(i) for i in self.tweet_ped])])


def load_data(filename, topic):
	tweet_list = []
	with open(filename) as input_file:
		for line in input_file:
			tweet = Tweet(topic)
			tweet.load(line)
			tweet_list.append(tweet)
	return tweet_list


def load_dic(path):
	with open(path) as inputfile:
		dic = pickle.load(inputfile)
	return dic


def calculate_pd(tweet_list, all_expand, topic, k1, b, avgdl):
	# TYPE_DIC = {'wiki':0, 'oldn':1, 'oldw':2, 'news50':3, 'web50':4, 'news20':5, 'web20':6}
	# all_expand['wiki'] = wiki_expand 
	# wiki_expand[topic] = [(q,tf,idf)]
	# self.tweet_ped = [0.0] * 7
	for tweet in tweet_list:
		for t in TYPE_DIC.keys():
			ped = 0
			pqd = 0
			for i in xrange(len(all_expand[t][topic])):
				f = tweet.get_word_list().count(all_expand[t][topic][i][0])
				c = f + k1 * (1 - b + b * len(tweet.get_word_list()) / float(avgdl))
				r = f * (k1 + 1) / float(c)
				qi = r * all_expand[t][topic][i][2]
				ped += qi
				if i < 10:
					pqd += qi
			tweet.set_tweet_pqd(pqd, TYPE_DIC[t])
			tweet.set_tweet_ped(ped, TYPE_DIC[t])
	return 0


def write_data(output_path, tweet_list):
	# 写入文件
	output_file = open(output_path, 'w')
	for tweet in tweet_list:
		output_file.write(tweet.print_tweet() + '\n')
	output_file.close()
	return 0


def tweet_sort(tweet_list):
	# 按天分组
	# 按bm25值排序
	# 相同的按时间先后排序
	_tweet_list = []
	tweet_list = sorted(tweet_list, key = lambda x: x.get_day())
	for k, v in groupby(tweet_list, key = lambda x: x.get_day()):
		day_list = sorted(list(v), key = lambda x: x.get_tweet_sumpqd(), reverse = True)
		for m, n in groupby(day_list, key = lambda x: x.get_tweet_sumpqd()):
			_tweet_list += sorted(list(n), key = lambda x: x.get_time())
	return _tweet_list


def remove_none(tweet_list):
	# 去掉0
	_tweet_list = []
	for tweet in tweet_list:
		if tweet.get_tweet_sumpqd() > 0:
			_tweet_list.append(tweet)
	return _tweet_list


def remove_repeat(tweet_list):
	# 去掉重复的
	_tweet_list = [tweet_list[0]]
	for tweet in tweet_list:
		if tweet.get_tweet_sumpqd() != _tweet_list[-1].get_tweet_sumpqd():
			_tweet_list.append(tweet)
			continue
		if tweet.get_word_list() == _tweet_list[-1].get_word_list():
			continue
		_tweet_list.append(tweet)
	return _tweet_list


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'calculate pqd,ped')
	parser.add_argument('-data', required = True, metavar = 'data', help = 'data file')
	parser.add_argument('-topic', required = True, metavar = 'topic', help = 'which topic')
	parser.add_argument('-output', required = True, metavar = 'output', help = 'output file')
	parser.add_argument('-all_expand', required = True, metavar = 'expand file', help = 'expand file')
	parser.add_argument('-k1', required = True, metavar = 'k1', help = 'bm25 k1')
	parser.add_argument('-b', required = True, metavar = 'b', help = 'bm25 b')
	parser.add_argument('-avg', required = True, metavar = 'avg', help = 'bm25 avg')

	args = parser.parse_args()
	data_path = vars(args)['data']
	topic = vars(args)['topic']
	output_path = vars(args)['output']
	all_expand_path = vars(args)['all_expand']
	k1 = float(vars(args)['k1'])
	b = float(vars(args)['b'])
	avgdl = float(vars(args)['avg'])

	all_expand = load_dic(all_expand_path)

	files = os.listdir(data_path)
	tweet_list = []
	for f in files:
		input_file_name = data_path + f
		tweet_list += load_data(input_file_name, topic)

	f1 = calculate_pd(tweet_list, all_expand, topic, k1, b, avgdl)
	print len(tweet_list)
	tweet_list = remove_none(tweet_list)
	print len(tweet_list)
	tweet_list = tweet_sort(tweet_list)
	print len(tweet_list)
	tweet_list = remove_repeat(tweet_list)
	print len(tweet_list)
	write_data(output_path, tweet_list)
