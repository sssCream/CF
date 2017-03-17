from dataset import dataset
from similarity import similarity

#user_base approach
#score of an item is proportional to similarities between
#user and other user

#p is a tuning tool to raise the importance of similar user
#when p = 1, score of an item is sum of similarity


class item_base_recommender:

	def __init__(self, dataset, similarity, n, p):
		self.dataset = dataset
		self.sim = similarity
		self.n = n

	def recommend(self, user):

		rank = {}

		for item in self.datast.user_item_matrix[user]:
			sim_items = self.sim.orderedSimilarity(item)[:self.n]

			for song, dist in sim_items:

				if song not in self.dataset.user_item_matrix[user]:

					if song not in rank:
						
						rank[song] = 0

					rank[song] += pow(dist, p)

		rec = sorted(rank.items(), key=lambda x: x[1], reverse=True)

		return rec

