#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


def cpk_calc(df_data: pd.DataFrame, usl, lsl):
    """
    :param df_data: 数据dataframe
    :param usl: 数据指标上限
    :param lsl: 数据指标下限
    :return:
    """
    sigma = 3
    # 若下限为0, 则使用上限反转负值替代
    if int(lsl) == 0:
        lsl = 0 - usl
 
    # 数据平均值
    u = df_data.mean()[0]
 
    # 数据标准差
    stdev = np.std(df_data.values, ddof=1)
 
    # 生成横轴数据平均分布
    x1 = np.linspace(u - sigma * stdev, u + sigma * stdev, 1000)
 
    # 计算正态分布曲线
    y1 = np.exp(-(x1 - u) ** 2 / (2 * stdev ** 2)) / (math.sqrt(2 * math.pi) * stdev)
 
    cpu = (usl - u) / (sigma * stdev)
    cpl = (u - lsl) / (sigma * stdev)
    # 得出cpk
    cpk = min(cpu, cpl)
 
    # 使用matplotlib画图
    plt.xlim(x1[0] - 0.5, x1[-1] + 0.5)
    plt.plot(x1, y1)
    plt.hist(df_data.values, 15, density=True)
    plt.title("cpk={0}".format(cpk))
    plt.show()

cpk_calc()