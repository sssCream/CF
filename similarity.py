'''
similarity.py

similarity class that calculate similarity matrix
based on given feature, feature data and model type
'''

'''
Note: can be cleaned up more
'''


import math
from dataset import dataset

#feature_type = count/binary [tfidf(not implemented)] 
#model_type = user_based/item_based



class similarity:
	def __init__(self, dataset, feature_type, model_type):
		self.dataset = dataset
		self.feature = feature_type
		self.model = model_type

		self.distance_method = self.cosine_binary if feature_type == 'binary' else self.cosine
			

		self.target_num_list = {}

		#construct num song list per user
		if(self.model == 'user'):
			self.numList(self.dataset.user_item_matrix)

		#construct num user list per song
		if(self.model == 'item'):
			self.numList(self.dataset.item_user_matrix)



	def numList(self, model_matrix):
		for target in model_matrix:
			self.target_num_list[target] = sum([count * count for count in model_matrix[target].values()])
			#e.g. user_item_matrix[user] = {"song1":1, "song2":2, "song3":3}
			#return target_num_list[user] -> 14 (= 1^2 + 2^2 + 3^2)


	#returned distance array of target sorted
	def orderedSimilarity(self, target):
		
		if(self.model == 'user'):
			sim = self.user_dist(target)

		if(self.model == 'item'):
			sim = self.item_dist(target)
		
		return sorted(sim.items(), key=lambda x: x[1], reverse = True)

	#compute distances of all other users to target(passed in user)
	def user_dist(self, user):	
		user_item_matrix = self.dataset.user_item_matrix
		item_user_matrix = self.dataset.item_user_matrix
		
		# find all users with at least one song in common:
		users_to_compute = set()
		for item in user_item_matrix[user]:
			for v in item_user_matrix[item]:
				if v != user:
					users_to_compute.add(v)
		
		#print users_to_compute
		# for all those users, compute the distance:
		distances = {}
		for v in users_to_compute:
			distances[v] = self.distance_method(user_item_matrix[user], user_item_matrix[v], user, v)
		
		return distances
		
	#compute distances of all other songs to target(passed in song)
	def item_dist(self, item):
		item_user_matrix = self.dataset.item_user_matrix
		user_item_matrix = self.dataset.user_item_matrix
		
		# find all items with at least one user in common:
		items_to_compute = set()
		for user in item_user_matrix[item]:
			for j in user_item_matrix[user]:
				if j != item:
					items_to_compute.add(j)
		
		# for all those users, compute the distance:
		distances = {}
		for j in items_to_compute:
			distances[j] = self.distance_method(item_user_matrix[item], item_user_matrix[j], item, j)
		
		return distances		
	
	def cosine(self, a_list, b_list, target_a, neighbor_b):
		dot_a_b = sum([a_list[item] * b_list[item] if item in b_list else 0 for item in a_list.iterkeys()])

		dist = 0;
		if dot_a_b > 0:
			dist = float(dot_a_b) / (math.pow(self.target_num_list[target_a], 0.5) * math.pow(self.target_num_list[neighbor_b], 0.5))
		return dist

	def cosine_binary(self, a_list, b_list, target_a, neighbor_b):
		dot_a_b = len(set(a_list) & set(b_list))

		dist = 0;
		if dot_a_b > 0:
			dist = float(dot_a_b) / (math.pow(self.target_num_list[target_a], 0.5) * math.pow(self.target_num_list[neighbor_b], 0.5))
		return dist



if __name__ == '__main__':
	#default feature type is binary
	dataset = dataset('triplets_test.txt')
	user_a = 60
	user_b = 57
	if user_a in dataset.user_item_matrix.keys():
		a = dataset.user_item_matrix[user_a]
		print 'user_a found'
		print a
	if user_a in dataset.user_item_matrix.keys():
		b = dataset.user_item_matrix[user_b]
		print 'user_b found'
		print b



	
	dist = similarity(dataset, 'binary', 'user')
	#print dist.target_num_list
	#print dist.model
	#print dist.feature
	print dist.cosine_binary(a, b, user_a, user_b)
	
	

	
	res1 = dist.orderedSimilarity(user_a)
	
	print len(res1)
	print res1[:5]
	
	'''
	users = sorted(dataset.user_item_matrix['binary'].iterkeys())
	n = len(users)
	'''

	'''
	
	sti = time.clock()
	i = 0
	
	sumLengths = 0
	minLengths = 99999999
	maxLengths = 0
	for user in users:
	
		i += 1
		if i % 100 == 00:
			cti = time.clock()
			t = cti - sti
			print "%d / %d) tot secs: %f (%f / user)"%(i, n, t,t/(i+1))
		
		nn = dist.nearestNeighboors(user)
		l = len(nn)
		sumLengths += l
		minLengths = min(l, minLengths)
		maxLengths = max(l, maxLengths)
	print sumLengths/len(users)
	print minLengths
	print maxLengths
	'''



	