import os

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]
filename = CUR_PATH + '/res.txt'

topics = 'MB226 MB229 MB230 MB239 MB254 MB256 MB258 MB265 MB267 MB276 MB286 ' + \
'MB319 MB320 MB332 MB351 MB358 MB361 MB362 MB363 MB365 MB371 MB377 MB381 MB382 ' + \
'MB391 MB392 MB409 MB410 MB414 MB420 MB425 MB431 MB436 MB438 MB440 ' + \
'RTS1 RTS10 RTS13 RTS14 RTS19 RTS2 RTS21 RTS24 RTS25 RTS27 RTS28 RTS31 RTS32 RTS35 RTS36 RTS37 RTS4 RTS43 RTS5 RTS6'
topic_list = topics.split(' ')

dic = {'wiki':{}, 'oldn':{}, 'oldw':{}, 'news50':{}, 'web50':{}, 'news20':{}, 'web20':{}}
dic = {'web50':{}}
t_list = ['pqd', 'pqded', 'pqdqcall', 'pqdqcvi', 'pqdqcedall', 'pqdqcedvi', 'pecall', 'pecvi', 'ped']

for k in dic.keys():
	for t in t_list:
		dic[k][t] = {}
		for topic in topic_list:
			dic[k][t][topic] = 0

with open(filename) as inputfile:
	for line in inputfile:
		kv = line.strip().split('      ')
		d = kv[3]
		n = kv[4]
		dic[kv[0]][kv[1]][kv[2]] = kv[5]

for k in dic.keys():
	print d, n
	print k, ' '.join(t_list)
	for topic in topic_list:
		print topic, 
		for t in t_list:
			print dic[k][t][topic],
		print ' '
	print ' '
	print ' '
