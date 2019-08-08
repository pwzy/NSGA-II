#!/usr/bin/python
# -*- coding:utf-8 -*-

from NSGA_II import *



def main():
    lowBound_list = [0, 0, 0, 0, 0, 0, 0]
    uppBound_list = [1, 1, 1, 1, 1, 1, 1]
    strFunctionType = "_TCH1"
    total_run = 1   # 代码运行的总次数
    max_gen = 1000   # 设置迭代的最大代数

    # 定义实例选择器DMOEA_DTLZ2_R1.dat
    instances = ["ZDT1","ZDT2","ZDT3","ZDT4","ZDT6","DTLZ1","DTLZ2"]
    nvars = [30, 30, 30, 10, 10, 10, 10]  # 定义每个测试实例变量的维度
    nobjs = [2, 2, 2, 2, 2, 3, 3]  # 定义每个测试实例目标维度

    # 分别对7个实例进行测试（迭代7次）
    for i in range(4,5):

        # 用来存储每个实例的名称
        strTestInstance = instances[i]

        # numVariables 存储变量维数
        numVariables = nvars[i]
        # numObjectives 存储变量维数
        numObjectives = nobjs[i]

        lowBound = lowBound_list[i]
        uppBound = uppBound_list[i]
        for run in range(1,total_run+1):

            # 创建对象
            MOEAD = TNSGAII(strTestInstance, numVariables, numObjectives, lowBound, uppBound)



            if numObjectives == 3:
                MOEAD.run(100, max_gen, run)
            if numObjectives == 2:
                MOEAD.run(100, max_gen, run)






if __name__=="__main__":
    main()