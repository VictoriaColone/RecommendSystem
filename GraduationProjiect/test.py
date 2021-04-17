from math import sqrt
from csv import *

users = {}
def trans_to_dict():
	'''读取csv转成dictionary'''
	with open('../ml-latest-small/ratings.csv', 'r')as csv_file:
		temp = '1'
		temp_dict = { }
		for i,line in enumerate(csv_file):
			row = line.split(',')
			if i != 0:
				if temp == row[0]:
					temp_dict[row[1]] = float(row[2])
				else:
					users[temp] = temp_dict
					temp = row[0]
					temp_dict = { }
					temp_dict[row[1]] = float(row[2])
class recommender:
	def __init__(self, data, k=1):
	   #以下变量将用于Slope One算法
	   	self.frequencies = {}
	   	self.deviations = {}
	   	self.k = k
	   	self.username2id = {}
	   	self.userid2name = {}
	   	self.productid2name = {}
	   	if type(data).__name__ == 'dict':
	   		self.data = data
	def convertProductID2name(self, id):
		if id in self.productid2name:
			return self.productid2name[id]
		else:
			return id
	def computeDeviations(self):
	   # 遍历嵌套字典获取每位用户的评分数据
		for ratings in self.data.values():
		# 对于该用户的每个评分项
			for (item, rating) in ratings.items():
				self.frequencies.setdefault(item, {})
				self.deviations.setdefault(item, {})
				# 再次遍历该用户的每个评分项
				for (item2, rating2) in ratings.items():
					if item != item2 :
						self.frequencies[item].setdefault(item2, 0)
						self.deviations[item].setdefault(item2, 0.0)
						self.frequencies[item][item2] += 1
						self.deviations[item][item2] += rating - rating2
		for (item, ratings) in self.deviations.items():
			for item2 in ratings:
				ratings[item2] /= self.frequencies[item][item2]
	def slopeOneRecommendations(self, userRatings):
		recommendations = {}
		frequencies = {}
		# 遍历目标用户的评分项
		for (userItem, userRating) in userRatings.items():
			# 对目标用户未评价的进行计算
			for (diffItem, diffRatings) in self.deviations.items():
				if diffItem not in userRatings and userItem in self.deviations[diffItem]:
					freq = self.frequencies[diffItem][userItem]
					recommendations.setdefault(diffItem, 0.0)
					frequencies.setdefault(diffItem, 0)
					#计算分子
					recommendations[diffItem] += (diffRatings[userItem] + userRating) * freq
					#计算分母
					frequencies[diffItem] += freq
		recommendations =  [(self.convertProductID2name(k),
							v / frequencies[k])
							for (k, v) in recommendations.items()]
		# 将其排序并返回
		recommendations.sort(key=lambda artistTuple: artistTuple[1],reverse = True)
		return recommendations
#test1
trans_to_dict()
# print(users)
#print(users.keys())
#输出字典中所有的键
r= recommender(users)
r.computeDeviations()
print(r.slopeOneRecommendations(users['3'])[0:5])
#输出推荐列表的前五个电影ID。