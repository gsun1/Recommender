#cosine.py - A first attempt at a cosine item-item recommender system
#The main problem this is trying to address is data sparsity

import codecs
from math import sqrt

#initialize recommendation builder
class rec_builder:
	def __init__(self, data = {}, k = 5, n = 3):
		if type(data).__name__ == 'dict': # make sure data is dictionary
			self.data = data # data contains the matrix of users and ratings
		self.k = k # This is the number of "nearest neighbors" for each item
		self.n = n # This is the number of recommendations given to each user
		places = [] # This is a list of all of the attractions featured in the data

	'''Loads data from a properly formatted CSV
	to the rec_builder instance
	'''
	def load(self, path):
		#initialize variables
		self.data = {}
		places = []
		num_places = 0
		#open file
		f = codecs.open(path)
		#loop through rows
		for line in f:
			#split rows by entry
			values = line.split(',')
			num_places = len(values)
			if not values[0]:
			#only first row empty
				for i in range(num_places):
					#add place to list of places
					places.append(values[i].strip())
			else:
				#user ID first entry in row
				user = values[0]
				#initialize user ratings variable
				self.data[user] = {}
				for i in range(1, num_places):
					if values[i]:
						#user went to and enjoyed place
						self.data[user][places[i]] = 1
					else:
						#user did not go or did not enjoy
						self.data[user][places[i]] = 0
		places.pop(0) #get rid of empty first column
		self.places = places

	'''Calculate cosine similarity between
	two attractions'''
	def cosine(self, i, j):
		#initialize variables
		dot_sum = 0.0
		mag_i = 0.0
		mag_j = 0.0
		#loop through values
		for user, values in self.data.items():
			#value for user of i is 1
			if values[i]:
				#add to sum of i's
				mag_i += 1
				'''if value for user at j
				is also 1'''
				if values[j]:
					#add to sum of j's
					mag_j += 1
					#add to numerator
					dot_sum += 1
			#value for user of i is 0
			else:
				'''if value for user of
				j is 1'''
				if values[j]:
					#add to sum of j's
					mag_j += 1
		#compute numerator/denominator
		denominator = (sqrt(mag_i * mag_j))
		if denominator:
			return dot_sum/denominator
		else:
			return 0

	#compute nearest k neighbors
	def nearest(self, i):
		#initialize varaibles
		neighbors = {}
		#loop through table
		for place in self.places:
			#ignore the place itself
			if place != i:
				#add to table
				neighbors[place] = self.cosine(i,place)
		#convert table to list for sorting
		neighbors = list(neighbors.items())
		neighbors.sort(key = lambda tuple: tuple[1], reverse = True)
		return neighbors[:self.k]

	#build table of nearest neighbors
	def build_table(self):
		#initialize variables
		self.ntable = {}
		#create entry for each place
		for place in self.places:
			self.ntable[place] = dict(self.nearest(place))

	'''predict a user's rating based on
	their ratings of other places'''
	def prediction(self,user,place):
		#initialize variables
		numerator = 0.0
		denominator = 0.0
		#loop through table, compute weighted average
		for name, similarity in self.ntable[place].items():
			numerator += similarity * self.data[user][name]
			denominator += similarity
		return numerator / denominator

	#recommend new places based on predictions
	def recommend(self,user):
		#initialize variables
		candidates = {}
		#loop thorugh places
		for place in self.places:
			#ignore places the user has already gone
			if not self.data[user][place]:
				#make prediction
				candidates[place] = self.prediction(user,place)
		#turn into list for sorting
		recommendations = list(candidates.items())
		recommendations.sort(key = lambda tuple: tuple[1], reverse = True)
		return recommendations[:self.n]

	def all_rec(self):
		frequencies = {}
		for user in self.data:
			print(user)
			rec = self.recommend(user)
			print(rec)
			for tup in self.recommend(user):
				if tup[0] in frequencies:
					frequencies[tup[0]] += 1
				else:
					frequencies[tup[0]] = 1
		print len(frequencies)
		print frequencies
		for place in self.places:
			if place not in frequencies:
				print(place)

r = rec_builder()

r.load('./mov.csv')
r.build_table()
r.all_rec()
