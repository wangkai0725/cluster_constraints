# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20180628
# File Name: rerank.py
# Description: 排序
"""
import argparse
import sys
import numpy
import gensim
from tweet import Tweet
from itertools import groupby
reload(sys)
sys.setdefaultencoding('utf-8')


def load_data(path):
	tweet_list = []
	with open(path) as input_file:
		for line in input_file:
			tweet = Tweet()
			tweet.load_rerank(line)
			tweet_list.append(tweet)
	return tweet_list


def write_data(output_path, tweet_list):
	# 按格式输出
	output_file = open(output_path, 'w')
	for tweet in write_list:
		output_file.write(tweet.print_formal_tweet() + '\n')
	output_file.close()
	return 0


def rescore_sort(day_tweet_list):
	# 按rescore排序
	write_list = []
	for day_list in day_tweet_list:
		write_list += sorted(day_list, key = lambda x: x.get_rescore(), reverse = True)[0:10]
	return write_list


def simhash_sort(day_tweet_list):
	# 按simhash去重
	# 这里用128位，海明距离12做临界
	write_list = []
	for day_list in day_tweet_list:
		i = 0
		# 结果条数
		for tweet in day_list:
			flag = 1
			for write in write_list:
				if hamming_distance(tweet.get_word_list(), write.get_word_list()) < 23 or len(tweet.get_word_list()) < 3:
					flag = 0
					break
			if flag:
				write_list.append(tweet)
				i += 1
				if i == 10:
					break
		j = 0
		# 列表指针
		while i != 10:
			# 当天不足10条的情况
			# 暂时用bm25补
			# 或者调大海明距离阈值
			if day_list[j] not in write_list:
				write_list.append(day_list[j])
				i += 1
			j += 1
	return write_list


def hamming_distance(word_list1, word_list2):
	# 海明距离
	x = (simhash(word_list1) ^ simhash(word_list2)) & ((1 << 128) - 1)
	tot = 0;
	while x :
		tot += 1
		x &= x - 1
	return tot


def simhash(word_list):
	# simhash值
	v = [0] * 128
	for t in [hash_fun(word) for word in word_list]:
		for i in range(128):
			bitmask = 1 << i
			if t & bitmask :
				v[i] += 1
			else:
				v[i] -= 1
	fingerprint = 0
	for i in range(128):
		if v[i] >= 0:
			fingerprint += 1 << i
	return fingerprint


def hash_fun(word):
	# 抄来的哈希函数
	if word == "":
		return 0
	else:
		x = ord(word[0]) << 7
		m = 1000003
		mask = 2 ** 128 - 1
		for c in word:
			x = ((x * m) ^ ord(c)) & mask
		x ^= len(word)
		if x == -1:
			x = -2
		return x


def word2vec_sort(day_tweet_list):
	# 按word2vec去重
	word2vec = gensim.models.word2vec.Word2Vec.load('E:\\GitHub\\workspace2\\src\\wiki.en.text.model')
	write_list = []
	for day_list in day_tweet_list:
		i = 0
		# 结果条数
		for tweet in day_list:
			flag = 1
			for write in write_list:
				if word2vec_cos_distance(tweet.get_word_list(), write.get_word_list(), word2vec) >= 0.8:
					flag = 0
					break
			if flag:
				write_list.append(tweet)
				i += 1
				if i == 10:
					break
		j = 0
		# 列表指针
		while i != 10:
			# 当天不足10条的情况
			# 暂时用bm25补
			if day_list[j] not in write_list:
				write_list.append(day_list[j])
				i += 1
			j += 1
	return write_list


def word2vec_cos_distance(word_list1, word_list2, word2vec):
	array1 = transformer_array_word2vec(word_list1, word2vec)
	array2 = transformer_array_word2vec(word_list2, word2vec)
	cos = numpy.dot(array1, array2.transpose()) / (numpy.linalg.norm(array1) * numpy.linalg.norm(array2))
	cos = 0.5 + 0.5 * cos
	return cos


def transformer_array_word2vec(word_list, word2vec):
	array = numpy.zeros((400, ))
	lens = 0
	for word in word_list:
		try:
			a = word2vec[word]
			array += a
			lens += 1
		except:
			pass
	if lens != 0:
		array /= float(lens)
	return array


def group_sort(tweet_list, expand):
	# 排序，按天分组
	# 是为了补足每天10条方便
	_tweet_list = []
	tweet_list = sorted(tweet_list, key = lambda x: x.get_day())
	for k, v in groupby(tweet_list, key = lambda x: x.get_day()):
		_tweet_list.append(sorted(list(v), key = lambda x: x.get_tweet_pqd(), reverse = True))
	return _tweet_list


def pqd_sort(day_tweet_list, expand):
	_day_tweet_list = []
	for day_list in day_tweet_list:
		for tweet in day_list:
			tweet.set_rescore(tweet.get_tweet_pqd())
			# tweet.set_rescore(tweet.get_tweet_sumpqd())
		_day_tweet_list.append(sorted(day_list, key = lambda x: x.get_rescore(), reverse = True))
	return _day_tweet_list


def ped_sort(day_tweet_list, expand):
	_day_tweet_list = []
	for day_list in day_tweet_list:
		for tweet in day_list:
			tweet.set_rescore(tweet.get_tweet_ped())
			# tweet.set_rescore(tweet.get_tweet_sumpqd())
		_day_tweet_list.append(sorted(day_list, key = lambda x: x.get_rescore(), reverse = True))
	return _day_tweet_list


def pqdqc_all_sort(day_tweet_list, expand):
	_day_tweet_list = []
	for day_list in day_tweet_list:
		for tweet in day_list:
			tweet.set_rescore(tweet.get_tweet_pqd() * tweet.get_tweet_pqc_all())
		_day_tweet_list.append(sorted(day_list, key = lambda x: x.get_rescore(), reverse = True))
	return _day_tweet_list


def pqdqc_vi_sort(day_tweet_list, expand):
	_day_tweet_list = []
	for day_list in day_tweet_list:
		for tweet in day_list:
			tweet.set_rescore(tweet.get_tweet_pqd() * tweet.get_tweet_pqc_centroid())
		_day_tweet_list.append(sorted(day_list, key = lambda x: x.get_rescore(), reverse = True))
	return _day_tweet_list


def pqded_sort(day_tweet_list, expand):
	_day_tweet_list = []
	for day_list in day_tweet_list:
		for tweet in day_list:
			tweet.set_rescore(tweet.get_tweet_pqd() * tweet.get_tweet_ped())
		_day_tweet_list.append(sorted(day_list, key = lambda x: x.get_rescore(), reverse = True))
	return _day_tweet_list


def pqdqced_all_sort(day_tweet_list, expand):
	_day_tweet_list = []
	for day_list in day_tweet_list:
		for tweet in day_list:
			tweet.set_rescore(tweet.get_tweet_pqd() * tweet.get_tweet_ped() * tweet.get_tweet_pqc_all())
		_day_tweet_list.append(sorted(day_list, key = lambda x: x.get_rescore(), reverse = True))
	return _day_tweet_list


def pqdqced_vi_sort(day_tweet_list, expand):
	_day_tweet_list = []
	for day_list in day_tweet_list:
		for tweet in day_list:
			tweet.set_rescore(tweet.get_tweet_pqd() * tweet.get_tweet_ped() * tweet.get_tweet_pqc_centroid())
		_day_tweet_list.append(sorted(day_list, key = lambda x: x.get_rescore(), reverse = True))
	return _day_tweet_list


def pec_vi_sort(day_tweet_list, expand):
	for day_list in day_tweet_list:
		for tweet in day_list:
			tweet.set_rescore(tweet.get_tweet_pec_centroid())
	_day_tweet_list = []
	for day_list in day_tweet_list:
		new_list = []
		_day_list = sorted(day_list, key = lambda x: x.get_rescore(), reverse = True)
		for k, v in groupby(_day_list, key = lambda x: x.get_rescore()):
			new_list += sorted(list(v), key = lambda x: x.get_tweet_pqd(), reverse = True)
		_day_tweet_list.append(new_list)
	return _day_tweet_list


def pec_all_sort(day_tweet_list, expand):
	for day_list in day_tweet_list:
		for tweet in day_list:
			tweet.set_rescore(tweet.get_tweet_pec_all())
	_day_tweet_list = []
	for day_list in day_tweet_list:
		new_list = []
		_day_list = sorted(day_list, key = lambda x: x.get_rescore(), reverse = True)
		for k, v in groupby(_day_list, key = lambda x: x.get_rescore()):
			new_list += sorted(list(v), key = lambda x: x.get_tweet_pqd(), reverse = True)
		_day_tweet_list.append(new_list)
	return _day_tweet_list


def calculate_rescore(day_tweet_list, expand, t):
	if t == 'pqd':
		return pqd_sort(day_tweet_list, expand)
	if t == 'pqdqcall':
		return pqdqc_all_sort(day_tweet_list, expand)
	if t == 'pqdqcvi':
		return pqdqc_vi_sort(day_tweet_list, expand)	
	if t == 'pqded':
		return pqded_sort(day_tweet_list, expand)
	if t == 'pqdqcedall':
		return pqdqced_all_sort(day_tweet_list, expand)
	if t == 'pqdqcedvi':
		return pqdqced_vi_sort(day_tweet_list, expand)
	if t == 'pecall':
		return pec_all_sort(day_tweet_list, expand)
	if t == 'pecvi':
		return pec_vi_sort(day_tweet_list, expand)
	if t == 'ped':
		return ped_sort(day_tweet_list, expand)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'sort script')
	parser.add_argument('-type', required = True, metavar = 'type', help = 'type')
	parser.add_argument('-expand', required = True, metavar = 'expand', help = 'expand')
	parser.add_argument('-input_path', required = True, metavar = 'data', help = 'data file')
	parser.add_argument('-output_path', required = True, metavar = 'output', help = 'output file')

	args = parser.parse_args()
	input_path = vars(args)['input_path']
	output_path = vars(args)['output_path']
	t = vars(args)['type']
	expand = vars(args)['expand']

	tweet_list = load_data(input_path)
	day_tweet_list = group_sort(tweet_list, expand)

	# ['pqd', 'pqdqc_all', 'pqded', 'pqdqced_all', 'pec_all', 'pqdqc_vi', 'pec_vi', 'pqdqced_vi']
	day_tweet_list = calculate_rescore(day_tweet_list, expand, t)
	write_list = simhash_sort(day_tweet_list)
	write_data(output_path, write_list)
