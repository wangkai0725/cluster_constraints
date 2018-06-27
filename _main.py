import os

CUR_PATH = os.path.split(os.path.realpath(__file__.split('/')[-1]))[0]

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
