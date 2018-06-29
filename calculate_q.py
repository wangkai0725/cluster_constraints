# - - coding:utf-8 - -
"""
# author: wktxzr
# Created Time : 20180503
# File Name: calculate_q.py
# Description: 
计算IDF
"""
import sys
import time
import math
import os
import pickle
import argparse
reload(sys)
sys.setdefaultencoding('utf-8')

class Tweet(object):
	def __init__(self, topic):
		self.tweet_id = ''
		self.tweet_word_list = []
		self.tweet_day = ''
		self.tweet_topic = topic
		self.tweet_bm25 = 0.0


	def load(self, line):
		l = line.strip().split('*')
		self.tweet_id = l[1]
		self.tweet_word_list = l[2].split(' ')
		self.tweet_day = '201608' + l[3].strip().split(' ')[2]


	def set_topic(self, topic):
		self.tweet_topic = topic


	def set_bm25(self, bm25):
		self.tweet_bm25 = bm25


	def get_id(self):
		return self.tweet_id


	def get_word_list(self):
		return self.tweet_word_list


	def get_day(self):
		return self.tweet_day


	def get_topic(self):
		return self.tweet_topic


	def get_bm25(self):
		return self.tweet_bm25


	def print_tweet(self):
		return '*'.join([self.tweet_id, ' '.join(self.tweet_word_list), self.tweet_day, self.tweet_topic, str(self.tweet_bm25)])


def load_data(filename, topic):
	tweet_list = []
	with open(filename) as input_file:
		for line in input_file:
			tweet = Tweet(topic)
			tweet.load(line)
			tweet_list.append(tweet)
	return tweet_list


def load_topic(path):
	p = open(path, 'rb')
	topic_dic = pickle.load(p)
	p.close()
	return topic_dic


def calculate_q(tweet_list, topic_word_list):
	# 计算IDF
	# 文档数
	N = len(tweet_list)
	# IDF
	# 格式 dic[word] = (tf, idf)
	qi_dic = {}
	for q in set(topic_word_list):
		nq = 0
		for tweet in tweet_list:
			if q in tweet.get_word_list():
				nq += 1
		qi_dic[q] = (topic_word_list.count(q), math.log(float(N + 0.5) / (nq + 0.5)))
	return qi_dic


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'calculate idf')
	parser.add_argument('-d', required = True, metavar = 'data', help = 'data file')
	parser.add_argument('-o', required = True, metavar = 'output', help = 'output file')
	parser.add_argument('-i', required = True, metavar = 'topic file', help = 'topic file')
	parser.add_argument('-w', required = True, metavar = 'topic', help = 'which topic')

	args = parser.parse_args()
	# data_path = CUR_PATH + '/init_data/'
	data_path = vars(args)['d']
	# output_path = CUR_PATH + '/' + topic + '.pkl'
	output_path = vars(args)['o']
	# topic_path = CUR_PATH + '/id_wikiexword_dic.pkl'
	topic_path = vars(args)['i']
	topic = vars(args)['w']

	topic_dic = load_topic(topic_path)
	files = os.listdir(data_path)
	tweet_list = []
	for f in files:
	 	input_file_name = data_path + f
	 	tweet_list += load_data(input_file_name, topic)
	# 显示用时
	start = time.clock()
	qi_dic = calculate_q(tweet_list, topic_dic[topic])
	with open(topic + '_qi_dic.pkl', 'wb') as outputfile:
		pickle.dump(qi_dic, outputfile)
	elapsed = (time.clock() - start)
	print 'done idf with ' + str(elapsed)
