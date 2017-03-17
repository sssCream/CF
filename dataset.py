'''dataset.py
dataset class that reads input data file
and create correspond data matrix and 
feature matrix.

constructor takes a file input, type of user_based feature 
and type of item_based feature. 
Or type default to be binary feature representation
'''

import math

class dataset:
	def __init__(self, input_file, user_feature_type='binary', item_feature_type='binary'):
		self.filename = input_file

		self.user_feature_type = user_feature_type
		self.item_feature_type = item_feature_type

		self.user2index = {}
		self.index2user = {}
		self.item2index = {}
		self.index2item = {}

		self.user_item_matrix = {}
		self.item_user_matrix = {}
		self.u2i_count = {}
		self.i2u_count = {}

		#load data from files
		self.load_user_indices()
		self.load_item_indices()
		self.load_matrices()


	def load_user_indices(self):
		print 'loading user indices...'
		f = open('kaggle_users.txt', 'r')
		i = 0
		for line in f:
			i += 1
			user = line.strip()
			self.user2index[user] = i
			self.index2user[i] = user
		f.close()
		print "done."
		
	
	def load_item_indices(self):
		print 'loading item indices...'
		f = open('kaggle_songs.txt', 'r')
		for line in f:
			item, i = line.strip().split(" ")
			i = int(i)
			self.item2index[item] = i
			self.index2item[i] = item
		f.close()
		print "done."


	def load_matrices(self):
		f = open(self.filename,'r')

		for row in f:
			user, item, count = row.strip().split('\t')
			count = int(count)

			user_index = self.user2index[user]
			item_index = self.item2index[item]

			#construct user_item_matrix
			#user -->row, item-->column
			if user_index not in self.user_item_matrix :
				self.user_item_matrix[user_index] = {}
				self.u2i_count[user_index] = {}


			#if 'count' == self.user_feature_type:
				#self.user_item_matrix[user_index][item_index] = count
			self.u2i_count[user_index][item_index] = count

			if 'binary' == self.user_feature_type:
				self.user_item_matrix[user_index][item_index] = 1

			if 'tfidf' == self.user_feature_type:
				self.user_item_matrix[user_index][item_index] = count


			#construct item_user_matrix
			#item-->row, user-->column

			if item_index not in self.item_user_matrix :
				self.item_user_matrix[item_index] = {}
				self.i2u_count[item_index] = {}
				

			#if 'count' == self.item_feature_type:
				#self.item_user_matrix[item_index][user_index] = count
			self.i2u_count[item_index][user_index] = count
				
			if 'binary' == self.item_feature_type:
				self.item_user_matrix[item_index][user_index] = 1

			if 'tfidf' == self.item_feature_type:
				self.item_user_matrix[item_index][user_index] = count

		if 'count' == self.item_feature_type:
			self.item_user_matrix = self.i2u_count

		if 'count' == self.user_feature_type:
			self.user_item_matrix = self.u2i_count




	
if __name__ == '__main__':
	'''
	matrix = dataset('triplets_test.txt', user_feature_type='binary');
	print matrix.user_item_matrix.keys()
	print matrix.item_user_matrix.keys()
	#input('...')
	'''
	