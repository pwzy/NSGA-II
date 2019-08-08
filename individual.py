#!/usr/bin/python
# -*- coding:utf-8 -*-
import random
from objective import *


class TIndividual:
    def __init__(self, strTestInstance, numVariables=30, numObjectives=2, lowBound=0, uppBound=1):
        # strTestInstance=""  实例名称
        # numVariables = 30  变量维度
        # numObjectives = 2
        # # 定义函上下界
        # lowBound = 0
        # uppBound = 1
        # x_var = range(30)
        # x_var = [ 0 for i in range(numVariables)]
        # y_obj = [ 0 for i in range(numObjectives)]
        # rank = 0  # pareto序号

        self.strTestInstance = strTestInstance
        self.numVariables = numVariables
        self.numObjectives = numObjectives
        # 传入测试函数定义域的上下界信息
        self.lowBound = lowBound
        self.uppBound = uppBound

        self.x_var = [0 for i in range(numVariables)]
        self.y_obj = [0 for i in range(numObjectives)]
        self.rank = 0
        # priority_select 选择优先级
        self.priority_select = 0
        # crow_distance 定义拥挤距离
        self.crowing_distance = 0
        # 定义支配本个体的个体数
        self.n_p = 0
        # 定义本个体支配的个体集合
        self.S_p = []

    # 实现种群中个体的随机初始化（每个维度为0 - 1之间的随机值）
    def rnd_init(self):
        for n in range(0, self.numVariables):
            self.x_var[n] = self.lowBound + random.random() * (self.uppBound - self.lowBound)
    # 计算自变量所对应的目标变量
    def obj_eval(self):
        self.y_obj = objectives(self.x_var, self.y_obj, self.strTestInstance, self.numVariables, self.numObjectives)

    #  显示目标变量的值
    def show_objective(self):
        for n in range(0, self.numObjectives):
            printf("%f ", y_obj[n])
        printf("\n")

    # 显示个体的值
    def show_variable(self):
        for n in range(0, self.numObjectives):
            printf("%f ", x_obj[n])
        printf("\n")

    # 定义支配判断函数
    def dominate_other(self, ind2):
        dominated = True
        for n in range(0, self.numObjectives):
            if ind2.y_obj[n] < self.y_obj[n]:
                dominated = False
                return False
        if ind2.y_obj == self.y_obj:
            dominated = False
            return False
        return dominated

    # 定义受支配判断函数  若被支配，则返回为真，否则返回假
    def was_dominated(self, ind2):
        was_dominated = True
        for n in range(0, self.numObjectives):
            if self.y_obj[n] < ind2.y_obj[n]:
                was_dominated = False
                return False
        if self.y_obj == ind2.y_obj:
            was_dominated = False
            return False
        return was_dominated


    # 计算支配本个体的个体数
    def n_p_eval(self, population):
        for n in range(len(population)):  # 遍历种群，为个体的n_p赋值
            if self.was_dominated(population[n]):
                self.n_p = self.n_p + 1

    def n_p_eval_reset(self):
        self.n_p = 0


    # 计算受本个体支配的个体的集合
    def S_p_eval(self, population):
        for n in range(len(population)):   # 遍历种群，找出本个体支配的个体集合
            if self.dominate_other(population[n]):
                self.S_p.append(population[n])

    def S_p_eval_reset(self):
        self.S_p = []









def main():
    pass
if __name__ == "__main_":
    main()