# -*- coding:utf-8 -*-
"""
# author: wktxzr
# Created Time : 20170505
# File Name: nmf.py
# Description: nmf类
"""
import numpy as np
import math

class Nmf(object):
	def __init__(self, data_array, a1, a2, d):
		self.array = data_array
		self.a1 = a1
		self.a2 = a2
		self.d = d

	def nmf(self):
		num_x, num_y = self.array.shape
		U = np.random.rand(num_x, self.d)
		V = np.random.rand(num_y, self.d)
		n_U = self._update_u(self.array, U, V, self.a1)
		n_V = self._update_v(self.array, U, V, self.a2)
		i = 1
		while self._isconvergent(self.array, self.a1, self.a2, n_U, n_V, U, V, i) != True:
			i += 1
			U = n_U.copy()
			V = n_V.copy()
			n_U = self._update_u(self.array, U, V, self.a1)
			n_V = self._update_v(self.array, U, V, self.a2)
		return n_U, n_V

	def _isconvergent(self, array, a1, a2, n_u, n_v, u, v, i):
		if i > 3000:
			return True
		if math.fabs(self._f_min(array, n_u, n_v, a1, a2) - self._f_min(array, u, v, a1, a2)) <= 10 ** (-5):
			return True
		else:
			return False

	def _f_min(self, array, u, v, a1, a2):
		f1 = np.linalg.norm((array - np.dot(u, v.transpose())), 'fro')
		f2 = a1 * np.linalg.norm(u, 'fro')
		f3 = a2 * np.linalg.norm(v, 'fro')
		return f1 + f2 + f3 

	def _update_u(self, array, u, v, a1):
		u1 = np.dot(array, v)
		u2 = np.dot(np.dot(u, v.transpose()), v) + a1 * u
		n_u = u * np.sqrt(u1 / (u2 + 1e-10))
		return n_u

	def _update_v(self, array, u, v, a2):
		v1 = np.dot(array.transpose(), u)
		v2 = np.dot(np.dot(v, u.transpose()), u) + a2 * v
		n_v = v * np.sqrt(v1 / (v2 + 1e-10))
		return n_v



class Regular_nmf(object):
	def __init__(self, data_array, a1, a2, a3, d, tweet_list):
		self.array = data_array
		self.a1 = a1
		self.a2 = a2
		self.a3 = a3
		self.d = d
		self.constraint = [t.get_tweet_pqd() for t in tweet_list]

	def r_nmf(self):
		num_x, num_y = self.array.shape
		U = np.random.rand(num_x, self.d)
		V = np.random.rand(num_y, self.d)
		Z = self._set_z(num_x, self.constraint)
		D = self._set_d(Z)
		n_U = self._update_u(self.array, U, V, Z, D, self.a1, self.a3)
		n_V = self._update_v(self.array, U, V, self.a2)
		i = 1
		while self._isconvergent(self.array, self.a1, self.a2, self.a3, n_U, n_V, U, V, Z, D, i) != True:
			i += 1
			U = n_U.copy()
			V = n_V.copy()
			n_U = self._update_u(self.array, U, V, Z, D, self.a1, self.a3)
			n_V = self._update_v(self.array, U, V, self.a2)
		return n_U, n_V

	def _isconvergent(self, array, a1, a2, a3, n_u, n_v, u, v, z, d, i):
		if i > 3000:
			return True
		if math.fabs(self._f_min(array, n_u, n_v, z, d, a1, a2, a3) - self._f_min(array, u, v, z, d, a1, a2, a3)) <= 10 ** (-5):
			return True
		else:
			return False

	def _f_min(self, array, u, v, z, d, a1, a2, a3):
		f1 = np.linalg.norm((array - np.dot(u, v.transpose())), 'fro')
		f2 = a1 * np.linalg.norm(u, 'fro')
		f3 = a2 * np.linalg.norm(v, 'fro')
		f4 = a3 * np.trace(np.dot(np.dot(u.transpose(),(d - z)), u))
		return f1 + f2 + f3 + f4

	def _update_u(self, array, u, v, z, d, a1, a3):
		u1 = np.dot(array, v) + a3 * np.dot(z, u)
		u2 = np.dot(np.dot(u, v.transpose()), v) + a1 * u + a3 * np.dot(d, u)
		n_u = u * np.sqrt(u1 / (u2 + 1e-10))
		return n_u

	def _update_v(self, array, u, v, a2):
		v1 = np.dot(array.transpose(), u)
		v2 = np.dot(np.dot(v, u.transpose()), u) + a2 * v
		n_v = v * np.sqrt(v1 / (v2 + 1e-10))
		return n_v

	def _set_z(self, num_x, constraint):
		z = np.zeros((num_x,num_x))
		for i in range(num_x):
			for j in range(num_x):
				z[i][j] = math.exp((-1) * math.fabs(constraint[i] - constraint[j]))
		return z

	def _set_d(self, z):
		num_x,num_y = z.shape
		num = 0
		d = np.zeros((num_x,num_y))
		for i in range(num_x):
			for j in range(num_x):
				num += z[j][i]
			d[i][i] = num
			num = 0
		return d
