#!/usr/bin/python
# -*- coding:utf-8 -*-

import random
import math
from individual import *


def distanceArray(vec1, vec2, dim):
    sum = 0
    for n in range(dim):
        sum += (vec1[n]-vec2[n])*(vec1[n]-vec2[n])
    return math.sqrt(sum)
def distanceVector(vec1, vec2):
    sum = 0
    for n in range(len(vec1)):
        sum += (vec1[n]-vec2[n])*(vec1[n]-vec2[n])
    return math.sqrt(sum)
def norm_vector(x):
    sum = 0
    for i in range(len(x)):
        sum = sum + x[i]*x[i]
    return math.sqrt(sum)
def sum_vector(vec):
    sum = 0
    for i in range(len(vec)):
        sum = sum + vec[i]
    return sum
def innerproduct(vec1, vec2):
    sum = 0
    for i in range(len(vec1)):
        sum += vec[i]*vec2[i]
    return sum
# 将数组按从小到大排序，找到距离权重最小的m个向量的索引值并存储在idx的前m个数据中，距离存储在x数组中
def minfastsort(x, idx, n, m):  # n代表的是种群规模，m代表的是领域的大小
    for i in range(m):
        for j in range(i+1, n):
            if x[i] > x[j] :
                temp = x[i]
                x[i] = x[j]
                x[j] = temp
                id = idx[i]
                idx[i] = idx[j]
                idx[j] =  id


def fast_non_dominated_sort(population):
    F = []
    F_1 = []
    for i in range(len(population)):  # 对每个个体进行遍历
        population[i].n_p_eval_reset()
        population[i].S_p_eval_reset()
    for i in range(len(population)):  # 对每个个体进行遍历
        population[i].n_p_eval(population)
        population[i].S_p_eval(population)

        if population[i].n_p == 0:
            population[i].priority_select = 1  # 计算p_rank的值
            F_1.append(population[i])
    # F.append(F_1)
    i = 1
    # 采取动态变量名进行新建parrot前沿的集合
    while len(locals()['F_' + str(i)]) != 0:
        # 判断前沿面集合不为空的时候，将生成的非支配前沿集合加入到分层结构中
        F.append(locals()['F_' + str(i)])
        Q = []
        for p in locals()['F_' + str(i)]:  # 对F_i列表中的元素进行遍历  for p in F_1
            for q in p.S_p:  # 对F_i中的每个个体中的S_p集合进行遍历
                q.n_p = q.n_p - 1
                if q.n_p == 0:
                    q.priority_select = i + 1
                    Q.append(q)
        i = i + 1
        locals()['F_' + str(i)] = Q

    return F

# 按照目标值进行排序  将集合F_set中第i+1维度的目标值按照从小到大的顺序进行排列
def sort_by_objective_value(list, dim): # dim表示按照第dim+1维进行排列
    for i in range(len(list)-1):
        for j in range(len(list)-i-1):
            if list[j].y_obj[dim] > list[j+1].y_obj[dim]:
                list[j], list[j + 1] = list[j + 1], list[j]
    return list


# 按照拥挤度值进行排序，F_set[i].crow_distance的值越大，说明此个体所处的空间较为稀疏，排列的时候排在较前边，选择的时候优先级越高
def sort_by_crow_distance_value(list):
    for i in range(len(list)-1):
        for j in range(len(list)-i-1):
            if list[j].crowing_distance > list[j+1].crowing_distance:
                list[j], list[j + 1] = list[j + 1], list[j]
    list.reverse()
    return list

# 定义计算拥挤距离的函数
def crowing_ditance_eval_and_sort(F_set, numObjectives):  # F_set代表要计算的层的集合（F_set为一个列表）
    l = len(F_set)  # l保存的额是F_set列表的长度
    # 每次计算的时候先对拥挤距离进行清零后再计算，防止以前的值对此时的拥挤距离造成的影响
    for k in range(0, l):
        F_set[k].crowing_distance = 0
    for i in range(numObjectives):  # 对于每一个目标对象而言进行操作, 对第i维进行研究
        f_max = 0
        f_min = 0

        F_set = sort_by_objective_value(F_set, i)  # 按照目标值从小到大进行升序排列进行排序
        f_max = F_set[l-1].y_obj[i]
        f_min = F_set[0].y_obj[i]

        # 将边界点的值设置为无穷大
        F_set[0].crowing_distance = 1e+30
        F_set[l - 1].crowing_distance = 1e+30
        # F_set[0].crowing_distance = 1e+30
        # F_set[l-1].crowing_distance = 1e+30
        # 对其他的点进行操作
        for j in range(1, l-1):
            F_set[j].crowing_distance = F_set[j].crowing_distance + \
                                        (F_set[j+1].y_obj[i]-F_set[j-1].y_obj[i])/(f_max-f_min+(1e-30))
    # 拥挤度计算完成，接下来按照拥挤度值从小到大进行元素的排序
    F_set = sort_by_crow_distance_value(F_set)  # # 按照拥挤度值进行排序,拥挤距离越大，说明排序的优先级越高

    return F_set  # 返回的F_set集合代表将原始的F_set集合按照拥挤度大小从小到大进行排列



# 从组合集合中选择个体
def select_ind_by_crowded_comparision_operator(F, pops, numObjectives):
    i = 0
    Population_next = []
    while len(Population_next)+len(F[i]) <= pops:   # until the parent population is filled
        Population_next.extend(F[i])
        i = i + 1
    if len(Population_next) < pops: # 此时说明下一代还没有填充满
        # 对第i+1层的元素进行排序
        F[i] = crowing_ditance_eval_and_sort(F[i], numObjectives)  # 对第i+1层的元素进行排序
        lack_num = pops - len(Population_next)  # 离填充满下一代种群还差lack_num个个体
        for j in range(0, lack_num):
            Population_next.append(F[i][j])
    return Population_next


    # 进行第i+1层元素的选择





def main():
    pass


if __name__=="__main__":
    main()