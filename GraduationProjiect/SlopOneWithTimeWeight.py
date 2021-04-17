# slope-one 生成融合时间权重的用户行为csv文件

import math
import random
from GraduationProjiect import ItemCF
from GraduationProjiect.CsvUtils import loadFile
from csv import *

class SlopOneWithTimeWeight():
    # 初始化相关参数
    def __init__(self):
        # 将数据集划分为训练集和测试集
        self.mTrainSet = {}
        self.mTestSet = {}

        # 用户所看过的电影集合
        self.userMovieSet = {}
        # 看过电影的用户集合
        self.movieUserSet = {}

        # 填充前后后矩阵
        self.mInitMatrix = {}
        self.mResultMatrix = []

    # 读文件得到“用户-电影”数组，格式：{'userid' :  {'movieid' : rating}}
    #
    # 得到用户电影索引/倒排索引字典，格式：{'userid':  {'movieid' : rating, 'movieid2' : rating}}
    #
    # 按格式获取数据
    def get_dataset(self, filename, pivot=0.0001):
        for line in loadFile(filename):
            user, movie, rating, timestamp = line.split(',')
            if(random.random() < pivot):
                # 训练集处理，包括生出初始矩阵、建立用户电影索引集合和倒排索集合
                self.mTrainSet.setdefault(user, {})[movie] = rating
                self.userMovieSet.setdefault(user, {})[movie] = [rating, timestamp]
                self.movieUserSet.setdefault(movie, {})[user] = [rating, timestamp]

            else:
                # 测试集处理，读取出数据即可
                self.mTestSet.setdefault(user, {})[movie] = rating
        print('Get trainingSet and testSet success!')

    # 计算物品之间评分差
    def cal_item_avg_diff(self):
        avgs_dict = {}
        for item1 in self.movieUserSet.keys():
            for item2 in self.movieUserSet.keys():
                avg = 0.0
                user_count = 0
                if item1 != item2:
                    for user in self.userMovieSet.keys():
                        user_rate = self.userMovieSet[user]
                        if item1 in user_rate.keys() and item2 in user_rate.keys():
                            user_count += 1
                            # 加上时间权重
                            avg += (float(user_rate[item1][0]) - float(user_rate[item2][0])) * \
                                   math.exp( - abs(int(user_rate[item1][1]) - int(user_rate[item1][1])))
                            avg = avg / user_count
                            avgs_dict.setdefault(item1, {})
                            avgs_dict[item1][item2] = avg
        print('Get cal_item_avg_diff success!')

        return avgs_dict

    # 计算两个电影的共同评分人数
    def item_both_rate_user(self, item1, item2):
        count = 0
        for user in self.userMovieSet.keys():
            if item1 in self.userMovieSet[user].keys() and item2 in self.userMovieSet[user].keys():
                count += 1
        return count

    # 预估评分并回填
    def predict_create_csv(self, avgs_dict):
        total = 0.0  # 分子
        count = 0  # 分母
        for user in self.userMovieSet.keys():
            # 递归所有电影，生成目标电影
            for itemAim in self.movieUserSet.keys():
                # 用户评价过电影
                for item in self.userMovieSet[user].keys():
                    if itemAim != item:
                        num = self.item_both_rate_user(itemAim, item)
                        count += num
                        total += num * (self.userMovieSet[user][itemAim] - avgs_dict[itemAim][item])
                        self.mTrainSet.append([user, itemAim, total/count])
        print('Get predict_create_csv success!')

if __name__ == '__main__':
    rating_file = '../ml-latest-small/ratings.csv'
    slopOneWithTimeWeight = SlopOneWithTimeWeight()
    slopOneWithTimeWeight.get_dataset(rating_file)
    slopOneWithTimeWeight.cal_item_avg_diff()
    # slopOneWithTimeWeight.predict_create_csv(slopOneWithTimeWeight.cal_item_avg_diff())
    # itemCF = ItemCF.ItemBasedCF(slopOneWithTimeWeight.mTrainSet, slopOneWithTimeWeight.mTestSet)
    # itemCF.calc_movie_sim()
    # itemCF.evaluate()