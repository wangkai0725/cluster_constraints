# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20170504
# File Name: tweet.py
# Description: tweet类
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Tweet(object):
	def __init__(self):
		self.tweet_id = ''
		self.tweet_word_list = []
		self.tweet_day = ''
		# 时间戳
		self.tweet_time = ''
		# 主题id
		self.tweet_topic = ''
		# 聚类结果
		self.tweet_clu = -1
		# p(q|d) query， 文档 
		self.tweet_pqd = 0
		# p(e|d) expand，文档
		self.tweet_ped = 0
		# p(q|clu) query，合并聚类文档
		self.tweet_pqc_all = 0
		# p(q|clu) query，类簇质心
		self.tweet_pqc_centroid = 0
		# p(e|clu) expand，合并聚类文档
		self.tweet_pec_all = 0
		# p(e|clu) expand，类簇质心
		self.tweet_pec_centroid = 0
		self.tweet_rescore = 0
		

	def load(self, line):
		# 760509510989471745*strong quilters*20160802*1470125771.0*MB226*24.8888162456*24.8888162456
		l = line.strip().split('*')
		self.tweet_id = l[0]
		self.tweet_word_list = l[1].split(' ')
		self.tweet_day = l[2]
		self.tweet_time = float(l[3])
		self.tweet_topic = l[4]
		self.tweet_pqd = float(l[5])
		self.tweet_ped = float(l[6])


	def load_rerank(self, line):
		l = line.strip().split('*')
		self.tweet_id = l[0]
		self.tweet_word_list = l[1].split(' ')
		self.tweet_day = l[2]
		self.tweet_time = float(l[3])
		self.tweet_topic = l[4]
		self.tweet_clu = l[5]
		self.tweet_pqd = float(l[6])
		self.tweet_ped = float(l[7])
		self.tweet_pqc_all = float(l[8])
		self.tweet_pqc_centroid = float(l[9])
		self.tweet_pec_all = float(l[10])
		self.tweet_pec_centroid = float(l[11])


	def set_id(self, _id):
		self.tweet_id = _id


	def get_id(self):
		return self.tweet_id


	def set_rescore(self, _rescore):
		self.tweet_rescore = _rescore


	def get_rescore(self):
		return self.tweet_rescore


	def set_word_list(self, _word_list):
		self.tweet_word_list += _word_list


	def get_word_list(self):
		return self.tweet_word_list


	def set_day(self, _day):
		self.tweet_day = _day


	def get_day(self):
		return self.tweet_day


	def set_time(self, _time):
		self.tweet_time = _time


	def get_time(self):
		return self.tweet_time


	def set_topic(self, _topic):
		self.tweet_topic = _topic


	def get_topic(self):
		return self.tweet_topic


	def set_clu(self, _clu):
		self.tweet_clu = _clu


	def get_clu(self):
		return self.tweet_clu


	def set_tweet_pqd(self, _pqd):
		self.tweet_pqd = _pqd


	def get_tweet_pqd(self):
		return self.tweet_pqd


	def set_tweet_ped(self, _ped):
		self.tweet_ped = _ped


	def get_tweet_ped(self):
		return self.tweet_ped


	def set_tweet_pqc_all(self, _pqc_all):
		self.tweet_pqc_all = _pqc_all


	def get_tweet_pqc_all(self):
		return self.tweet_pqc_all


	def set_tweet_pec_all(self, _pec_all):
		self.tweet_pec_all = _pec_all


	def get_tweet_pec_all(self):
		return self.tweet_pec_all


	def set_tweet_pqc_centroid(self, _pqc_centroid):
		self.tweet_pqc_centroid = _pqc_centroid


	def get_tweet_pqc_centroid(self):
		return self.tweet_pqc_centroid


	def set_tweet_pec_centroid(self, _pec_centroid):
		self.tweet_pec_centroid = _pec_centroid


	def get_tweet_pec_centroid(self):
		return self.tweet_pec_centroid


	def print_tweet(self):
		return '*'.join([self.tweet_id, ' '.join(self.tweet_word_list), \
			self.tweet_day, str(self.tweet_time), self.tweet_topic, str(self.tweet_clu), \
			str(self.tweet_pqd), str(self.tweet_ped), \
			str(self.tweet_pqc_all), str(self.tweet_pqc_centroid), \
			str(self.tweet_pec_all), str(self.tweet_pec_centroid)])


	def print_formal_tweet(self):
		# 计算ndcg的脚本要求格式
		return ' '.join([self.tweet_day, self.tweet_topic, 'Q0', self.tweet_id, str(self.tweet_pqd), str(self.tweet_rescore), self.tweet_clu])
