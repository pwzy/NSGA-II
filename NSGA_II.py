#!/usr/bin/python
# -*- coding:utf-8 -*-
import  random
import math
from individual import *
from  recombination import  *
from common import *
import test
from plot_image import plot_image
from plot_image import plot_image2

# 定义NSGA-II的类，用来控制NSGA—II算法的运行
class TNSGAII:
    # 定义构造函数
    def __init__(self, strTestInstance, numVariables=30, numObjectives=2, lowBound=0, uppBound=1):
     # 设置参数

     self.pops = 0  # 定义种群大小
     self.strTestInstance = strTestInstance
     self.numVariables = numVariables
     self.numObjectives = numObjectives
     # 传入测试函数定义域的上下界信息
     self.lowBound = lowBound
     self.uppBound = uppBound

     # 定义种群
     self.population = []

    # 定义初始化种群函数,即为种群中每个个体进行初始化
    def init_population(self, pop):
        for i in range(pop): # 一共初始化pop个个体
            # 新建一个新的个体对象
            sop = TIndividual(self.strTestInstance, self.numVariables,
                              self.numObjectives, self.lowBound, self.uppBound)
            # 初始化个体
            sop.rnd_init()
            sop.obj_eval()
            # 将新的个体增加到种群列表中
            self.population.append(sop)
        self.pops = len(self.population)


    def evolution(self, max_gen):
        for n in range(max_gen): # 在每一代的过程中
            print("迭代次数为：%d" % (n+1))
            # Q = []  # 定义产生的子种群 ，种群大小为self.pop
            # print(n)
            R = self.population
            Q = self.make_new_pop(self.population)
            Q1 = self.make_new_pop(self.population)
            Q2 = self.make_new_pop(self.population)
            R.extend(Q)
            R.extend(Q1)
            R.extend(Q2)
            # self.population.extend(Q) # 此时的self.population为合并的列表
            # 对合并的列表进行pareto分层,将合并的列表进行分层标记
            # 定义F为一个列表，保存的是合并种群的分层结构。
            F = []

            F = fast_non_dominated_sort(R)
            full_num = 0  # pop个数
            # for i in range(len(F)):    # 统计F中的个体数
            #     full_num = full_num + len(F[i])
            # print(full_num)

            P_next_generation = select_ind_by_crowded_comparision_operator(F, self.pops, self.numObjectives)
            self.population = P_next_generation

            # 画图观察
            if self.numObjectives == 2:
                if n % 50 == 0:
                    x = []
                    y = []
                    for j in range(len(self.population)):
                        x.append(self.population[j].y_obj[0])
                        y.append(self.population[j].y_obj[1])

                    plot_image2(x,y)
            else:
                # 画图观察
                if n % 50 == 0:
                    x = []
                    y = []
                    z = []
                    for j in range(len(self.population)):
                        x.append(self.population[j].y_obj[0])
                        y.append(self.population[j].y_obj[1])
                        z.append(self.population[j].y_obj[2])
                    plot_image(x, y, z)



        # print(len(self.population))



    # 定义根据父种群产生同样大小的子种群函数
    def make_new_pop(self, population):
        Q = []
        p1 = random.randrange(0, self.pops)  # r1代表生成0-s中的一个整数
        p2 = random.randrange(0, self.pops)  # r2代表生成0-s中的一个整数

        for i in range(int(self.pops/2)):  # 迭代产生子代,每迭代一次产生两个子代。
            child1 = TIndividual(self.strTestInstance, self.numVariables,
                              self.numObjectives, self.lowBound, self.uppBound)
            child2 = TIndividual(self.strTestInstance, self.numVariables,
                              self.numObjectives, self.lowBound, self.uppBound)
            child1, child2 = realbinarycrossover(self.population[p1], self.population[p2],
                                                self.numVariables, self.lowBound, self.uppBound, child1,
                                                child2)
            child1 = realmutation(child1, 1.0/self.numVariables, self.numVariables, self.lowBound, self.uppBound)
            child1.obj_eval()
            child2 = realmutation(child2, 1.0/self.numVariables, self.numVariables, self.lowBound, self.uppBound)
            child2.obj_eval()
            Q.append(child1)
            Q.append(child2)
        return Q






    # 定义运行函数，控制程序的运行
    def run(self, pop, mg, rn):
        # pop 代表种群规模，mg代表最大的迭代次数，rn代表程序的运行次数
        # 首先初始化一个种群
        self.init_population(pop)


        # 让种群进化
        self.evolution(mg)


        savefilename = "ParetoFront/NSGA-II_" + self.strTestInstance + "_R" + str(rn) + ".dat"
        self.save_front(savefilename)
        self.population.clear()

    # 定义保存pareto前沿的函数，用来保存运行后生成的Pareto前沿
    def save_front(self, saveFilename):
        target = open(saveFilename, mode='w+')
        for n in range(len(self.population)):
            for k in range(self.numObjectives):
                # target.writelines("%d  " % (self.population[n].indiv.y_obj[k]))
                target.writelines("%f  " % (self.population[n].y_obj[k]))
            # print(self.population[n].indiv.y_obj)
            target.writelines("\n")
        target.close()



def main():
    pass

if __name__ == "__main__":
    main()
