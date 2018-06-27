# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20170503

# File Name: cluster.py
# Description: 聚类
"""
import pickle
import sys
import math
import argparse
import nmf
import gensim
import numpy as np
from tweet import Tweet
from numpy import linalg
from itertools import groupby
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfTransformer as tt
from sklearn.feature_extraction.text import CountVectorizer as cv
reload(sys)
sys.setdefaultencoding('utf-8')

k1 = 2
b = 0.75
avgdl = 19
a1 = 0.01
a2 = 0.01
a3 = 0.01

def tweet_top(tweet_list):
	_tweet_list = []
	tweet_list = sorted(tweet_list, key = lambda x: x.get_day())
	for k, v in groupby(tweet_list, key = lambda x: x.get_day()):
		day_list = sorted(list(v), key = lambda x: x.get_tweet_pqd(), reverse = True)[0:100]
		_tweet_list += day_list
	return _tweet_list


def load_dic(path):
	with open(path) as inputfile:
		dic = pickle.load(inputfile)
	return dic


def load_data(filename):
	tweet_list = []
	with open(filename) as input_file:
		for line in input_file:
			tweet = Tweet()
			tweet.load(line)
			tweet_list.append(tweet)
	return tweet_list


def transformer_array_vsm(tweet_list):
	corpus = []
	for tweet in tweet_list:
		corpus.append(' '.join(tweet.get_word_list()))
	vectorizer = cv()
	transformer = tt()
	tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
	array = tfidf.toarray()
	word_list=vectorizer.get_feature_names()
	return array, word_list


def kmeans_cluster(data_array, d):
	'''
	这里本地修改了sklearn，将欧氏距离改为余弦相似度
	'''
	_kmeans = KMeans(n_clusters = d).fit(data_array)
	clu_res = _kmeans.labels_
	centroids = _kmeans.cluster_centers_
	# print metrics.calinski_harabaz_score(data_array, res)
	# print _kmeans.score(data_array, res)
	return clu_res, centroids


def nmf_cluster(data_array, d):
	_nmf = nmf.Nmf(data_array, a1, a2, d)
	U, V = _nmf.nmf()
	clu_res = _u_get_clu(U)
	return clu_res, V


def regular_nmf_cluster(data_array, d, tweet_list):
	_nmf = nmf.Regular_nmf(data_array, a1, a2, a3, d, tweet_list)
	U, V = _nmf.r_nmf()
	clu_res = _u_get_clu(U)
	return clu_res, V


def _u_get_clu(n_u):
	# 根据U得到每个tweet的类别
	clu_res = []
	x, y = n_u.shape
	for i in xrange(x):
		ind = 0
		max_pro = 0
		for j in xrange(y):
			if n_u[i][j] > max_pro:
				max_pro = n_u[i][j]
				ind = j
		clu_res.append(ind)
	return clu_res


def set_cluster_res(tweet_list, clu_res):
	if len(tweet_list) != len(clu_res):
		return 1
	for i in xrange(len(tweet_list)):
		tweet_list[i].set_clu(clu_res[i])
	return 0


def get_cluster_list(tweet_list):
	cluster_list = []
	_tweet_list = sorted(tweet_list, key = lambda x: x.get_clu())
	for clu_num, _group in groupby(_tweet_list, key = lambda x: x.get_clu()):
		clu = Tweet()
		clu.set_id(str(clu_num))
		clu.set_clu(clu_num)
		clu_tweet_list = list(_group) 
		for tweet in clu_tweet_list:
			clu.set_word_list(tweet.get_word_list())
		cluster_list.append(clu)
	return cluster_list


def get_centroid_list(centroids, array_word_list):
	centroid_list = []
	centroid_weight_list = []
	n, word_num = centroids.shape
	for i in xrange(n):
		clu = Tweet()
		clu.set_id(str(i))
		clu.set_clu(i)
		word_list = []
		word_weight = []
		for j in xrange(word_num):
			if centroids[i][j] > 0.001:
				word_list.append(array_word_list[j])
				word_weight.append(centroids[i][j])
		clu.set_word_list(word_list)
		centroid_list.append(clu)
		centroid_weight_list.append(word_weight)
	return centroid_list, centroid_weight_list


def calculate_pqc_pec_all(cluster_list, web_expand, topic):
	for cluster in cluster_list:
		pec = 0
		pqc = 0
		for i in xrange(len(web_expand[topic])):
			f = cluster.get_word_list().count(web_expand[topic][i][0])
			c = f + k1 * (1 - b + b * len(cluster.get_word_list()) / float(avgdl))
			r = f * (k1 + 1) / float(c)
			qi = r * web_expand[topic][i][2]
			pec += qi
			if i < 10:
				pqc += qi
		cluster.set_tweet_pec_all(pec)
		cluster.set_tweet_pqc_all(pqc)
	return 0


def calculate_pqc_pec_centroid(centroid_list, centroid_weight_list, web_expand, topic):
	for i in xrange(len(centroid_list)):
		pec = 0
		pqc = 0
		for j in xrange(len(web_expand[topic])):
			if web_expand[topic][j][0] in centroid_list[i].get_word_list():
				f = centroid_weight_list[i][centroid_list[i].get_word_list().index(web_expand[topic][j][0])]
			else:
				f = 0
			c = f + k1 * (1 - b + b * len(centroid_list[i].get_word_list()) / float(avgdl))
			r = f * (k1 + 1) / float(c)
			qi = r * web_expand[topic][j][2]
			pec += qi
			if j < 10:
				pqc += qi
		centroid_list[i].set_tweet_pec_centroid(pec)
		centroid_list[i].set_tweet_pqc_centroid(pqc)
	return 0


def set_pqc_pec_all(tweet_list, cluster_list):
	pec_dic = {}
	pqc_dic = {}
	for clu in cluster_list:
		pec_dic[clu.get_clu()] = clu.get_tweet_pec_all()
		pqc_dic[clu.get_clu()] = clu.get_tweet_pqc_all()
	for tweet in tweet_list:
		tweet.set_tweet_pec_all(pec_dic[tweet.get_clu()])
		tweet.set_tweet_pqc_all(pqc_dic[tweet.get_clu()])
	return 0


def set_pqc_pec_centroid(tweet_list, centroid_list):
	pec_dic = {}
	pqc_dic = {}
	for clu in centroid_list:
		pec_dic[clu.get_clu()] = clu.get_tweet_pec_centroid()
		pqc_dic[clu.get_clu()] = clu.get_tweet_pqc_centroid()
	for tweet in tweet_list:
		tweet.set_tweet_pec_centroid(pec_dic[tweet.get_clu()])
		tweet.set_tweet_pqc_centroid(pqc_dic[tweet.get_clu()])
	return 0


def wrtie_data(output_path, write_list):
	with open(output_path, 'w') as outputfile:
		for tweet in write_list:
			outputfile.write(tweet.print_tweet() + '\n')
	return 0


def load_model(modle_path):
	model = gensim.models.word2vec.Word2Vec.load(modle_path)
	return model


def transformer_array_word2vec(tweet_list, word2vec):
	array_list = []
	for tweet in tweet_list:
		array = np.zeros((400, ))
		lens = 0
		for word in tweet.get_word_list():
			try:
				a = word2vec[word]
				array += a
				lens += 1
			except:
				pass
		if lens != 0:
			array /= float(lens)
		array_list.append(array)
	return np.array(array_list)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'cluster script')
	parser.add_argument('-data', required = True, metavar = 'data', help = 'data file')
	parser.add_argument('-topic', required = True, metavar = 'topic', help = 'which topic')
	parser.add_argument('-output_tweet', required = True, metavar = 'output', help = 'output file')
	parser.add_argument('-all_expand', required = True, metavar = 'expand file', help = 'expand file')
	parser.add_argument('-word2vec_path', required = True, metavar = 'expand file', help = 'expand file')
	parser.add_argument('-n', required = True, metavar = 'n', help = 'cluster number')

	args = parser.parse_args()
	data_path = vars(args)['data']
	topic = vars(args)['topic']
	output_tweet = vars(args)['output_tweet']
	expand_path = vars(args)['all_expand']
	word2vec_path = vars(args)['word2vec_path']
	d = int(vars(args)['n'])

	tweet_list = load_data(data_path)
	# web_expand['topic'] = [[word, tf ,idf]..]
	web_expand = load_dic(expand_path)
	# 每天取前100tweet
	tweet_list = tweet_top(tweet_list)

	# 用word2vec表示
	# word2vec_model = load_model(word2vec_path)
	# data_array = transformer_array_word2vec(tweet_list, word2vec_model)


	# # # kmeans聚类
	# clu_res, centroids = kmeans_cluster(data_array, d)

	# # # nmf聚类
	# # clu_res, centroids = nmf_cluster(data_array, d)
	# # # 正则化nmf聚类
	# # # clu_res, centroids = regular_nmf_cluster(data_array, d, tweet_list)

	# # 结果写入tweet_list
	# flag0 = set_cluster_res(tweet_list, clu_res)
	# cluster_list = get_cluster_list(tweet_list)
	# # centroid_list, centroid_weight_list = get_centroid_list(centroids, array_word_list)

	# calculate_pqc_pec_all(cluster_list, web_expand, topic)
	# # calculate_pqc_pec_centroid(centroid_list, centroid_weight_list, web_expand, topic)
	# flag1 = set_pqc_pec_all(tweet_list, cluster_list)
	# # flag2 = set_pqc_pec_centroid(tweet_list, centroid_list)
	# flag3 = wrtie_data(output_tweet, tweet_list)



	# 将数据转换成向量，采用向量空间模型
	data_array, array_word_list = transformer_array_vsm(tweet_list)

	# kmeans聚类
	clu_res, centroids = kmeans_cluster(data_array, d)

	# nmf聚类
	# clu_res, centroids = nmf_cluster(data_array, d)
	# 正则化nmf聚类
	# clu_res, centroids = regular_nmf_cluster(data_array, d, tweet_list)

	# 结果写入tweet_list
	flag0 = set_cluster_res(tweet_list, clu_res)
	cluster_list = get_cluster_list(tweet_list)
	centroid_list, centroid_weight_list = get_centroid_list(centroids, array_word_list)

	calculate_pqc_pec_all(cluster_list, web_expand, topic)
	calculate_pqc_pec_centroid(centroid_list, centroid_weight_list, web_expand, topic)
	flag1 = set_pqc_pec_all(tweet_list, cluster_list)
	flag2 = set_pqc_pec_centroid(tweet_list, centroid_list)
	flag3 = wrtie_data(output_tweet, tweet_list)
