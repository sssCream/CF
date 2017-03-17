import numpy as np

f = open('kaggle_visible_evaluation_triplets.txt','r')
song_to_count = dict()
user_to_songs = dict()
user_song_count = dict()

for row in f:
	user, song, count = row.strip().split('\t')
	user_song_count[(user,song)] = int(count)
	#print(type(user_song_count))
	#print(str(user_song_count[(user,song)]) + ', ' + count)

	#dictionary{song:count}
	if song in song_to_count:
		song_to_count[song] +=1
	else:
		song_to_count[song] = 1

	#dictionary{user:([songs])}
	if user in user_to_songs:
		user_to_songs[user].add(song)
	else:
		user_to_songs[user] = set([song])

#List of str(songs) HIGHER --> LOWER
songs_ordered = sorted(song_to_count.keys(), key = lambda s: song_to_count[s], reverse = True)

#generate list of list, storing each user's listening count of each song
total_user_count = []
user_i = 0
for user in user_to_songs:
	user_count = []
	print('user' + str(user_i) + ' done')
	user_i += 1
	
	for song_x in range(len(songs_ordered)):
		if songs_ordered[song_x] in user_to_songs[user]:
			user_count.append(user_song_count[(user,songs_ordered[song_x])])
		else:
			user_count.append(0)
	total_user_count.append(user_count)
	
feature_array = np.array(total_user_count)
feature_matrix = np.asmatrix(feature_array)
#print(type(feature_matrix))
print(feature_matrix)
# print(songs_ordered[0:50])
# print(total_user_count[0:30])


f.close()