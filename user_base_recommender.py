from dataset import dataset
from similarity import similarity

#user_base approach
#score of an item is proportional to similarities between
#user and other user

#p is a tuning tool to raise the importance of similar user
#when p = 1, score of an item is sum of similarity


class user_base_recommender:

	def __init__(self, dataset, similarity, n, p):
		self.dataset = dataset
		self.sim = similarity
		self.n = n

	def recommend(self, user):
		similar_users = self.sim.orderedSimilarity(user)[:self.n]

		rank = {}

		#Iterate through n number of similar users to (target)user
		for sim_user,dist in similar_users:
			#for each song each similar user has listened to, (give each song a score)
			for item in self.dataset.user_item_matrix[sim_user]:
				#if target user hasn't heard this song
				if item not in self.data.user_item_matrix[user]:
					#if item not (a key) in (rank)map, add it
					if item not in rank:
						rank[item] = 0;

				#scoring function
				#distance(user, sim_user)*log(count of song sim_user listen to)
				#add in p parameter and song count to help scoring better, 
				#emphasizing songs 
				#could try different scoring function
				
				#simple scoring fucntion
				#rank[item += pow(dist, p)
				rank[item] += pow(dist * math.log(self.dataset.u2i_count[sim_user][item]), p)

		#sorted by value(score) from largest to smallest
		#returned rec is a list of tuple=('song ide', score)
		rec = sorted(rank.items(), key=lambda x: x[1], reverse=True)
			
		
		return rec
