#!//Users/gregorysun/anaconda3/bin/python3

import codecs

'''calculate the general minkowski distance between two items in
ratings space note that:
r = 1 is Manhattan distance
r = 2 is Euclidean distance
r = 3 is supremum distance'''
def minkowski(data, item1, item2, r):
	result = 0.0
	#loop through all ratings dimensions, and add accordingly
	for quality in data[item1]:
		result += abs(data[item1][quality] - data[item2][quality]) ** r
	result = result ** (1.0/r)
	return result

'''calculates the minkowski distance between two items
in two different datasets. Assumes that the datasets have
the same general format'''
def cross_minkowski(data1, data2, item1, item2, r):
	result = 0.0
	for quality in data1[item1]:
		result += abs(data1[item1][quality] - data2[item2][quality]) ** r
	result = result ** (1.0/r)
	return result

'''Recommender system class. Works within a single dataset'''
class recommender:

	'''Initialization method
	k = number of recomendations per place
	r = r in minkowski distance formula'''
	def __init__(self, k = 3, r = 2):
		self.k = k
		self.r = r

	'''loads data into system'''
	def load(self, path):
		num_qualities = 0
		self.data = {}
		qualities = []
		#iterate through each line of file
		for line in open(path):
			values = line.split(',')
			#only first line has empty first entry
			#first line is where the places are stored
			if values[0] == '':
				num_qualities = len(values)
				for value in values:
					qualities.append(value.strip())
			else:
				#build dictionary based on entries
				#each rating should be in the same
				#numbered position as the place in line 1
				place = values[0]
				self.data[place] = {}
				for i in range(1,num_qualities):
					self.data[place][qualities[i]] = int(values[i])
		qualities.pop(0)
		self.qualities = qualities

	'''Calculates nearest k neighbors based on loaded data
	Method should not be called until after load method'''
	def nearest_k(self,item):
		candidates = []
		#loop thorugh data
		for place in self.data:
			if place != item:
				#add tuple containing distance and location name
				candidates.append((minkowski(self.data,item,place,self.r),place))
		#use distance entry in tuple to sort
		candidates.sort(key = lambda tuple: tuple[0], reverse = False)
		return candidates[:self.k]

	'''Builds a recommendation table mapping each place
	to an ordered list of the nearest k places'''
	def build_rec_table(self):
		self.rec_table = {}
		for place in self.data:
			self.rec_table[place] = []
			#get recommendations
			recs = self.nearest_k(place)
			#strip distance data from tuple
			for rec in recs:
				self.rec_table[place].append(rec[1])

	'''prints out all recommendations in a readable format'''
	def get_recommendations(self,place):
		print("If you liked {!s}, you might also like:".format(place))
		print(self.rec_table[place])

'''Handles recommendations between datasets'''
class cross_recommender:

	#load the two recommendation systems to create class
	def __init__(self, rec1, rec2, k = 3, r = 2):
		self.rec1 = rec1
		self.rec2 = rec2
		self.k = k
		self.r = r

	'''Like nearest_k in the recomendation class, but this
	time, will find the nearest k from rec{num} where
	num is 1 or 2'''
	def nearest_k(self, num, item):
		candidates = []
		if num == 1:
			for place in self.rec2.data:
				candidates.append((cross_minkowski(self.rec1.data, self.rec2.data, item,place,self.r),place))
		else:
			for place in self.rec1.data:
				candidates.append((cross_minkowski(self.rec2.data, self.rec1.data, item,place,self.r),place))
		candidates.sort(key = lambda tuple: tuple[0], reverse = False)
		return candidates[:self.k]

	'''Builds two tables. Table 1 takes all of the places
	in dataset 1 and suggests top k closest places in dataset 2.
	Table 2 takes all of the places in dataset 2 and suggests the
	top k closest places in dataset 1.'''
	def build_cross_tables(self):
		self.t1 = {}
		self.t2 = {}
		for place in self.rec1.data:
			self.t1[place] = []
			recs = self.nearest_k(1, place)
			for rec in recs:
				self.t1[place].append(rec[1])
		for place in self.rec2.data:
			self.t2[place] = []
			recs = self.nearest_k(2, place)
			for rec in recs:
				self.t2[place].append(rec[1])

	'''Prints recommendations in readable format'''
	def get_recommendations(self, num, place):
		print("If you liked {!s}, you might also like:".format(place))
		if num == 1:
			print(self.t1[place])
		else:
			print(self.t2[place])
		print()


#Tests with sample data
r1 = recommender()
r1.load('chicago.csv')
r1.build_rec_table()
r2 = recommender()
r2.load('nyc.csv')
r2.build_rec_table()
c = cross_recommender(r1, r2)
c.build_cross_tables()
for place in c.rec1.data:
	c.get_recommendations(1, place)

for place in c.rec2.data:
	c.get_recommendations(2, place)