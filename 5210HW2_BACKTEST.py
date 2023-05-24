# -*- coding: utf-8 -*-
"""
Created on Wed May 24 15:05:49 2023

@author: dell
"""

# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals
from sklearn.linear_model import LinearRegression
import multiprocessing
import numpy as np
import pandas as pd
from gm.api import *



# 获取每次回测的报告数据
def on_backtest_finished(context, indicator):
    data = [indicator['pnl_ratio'], indicator['pnl_ratio_annual'], indicator['sharp_ratio'], indicator['max_drawdown'],
            context.num]
    # 将超参加入context.result
    context.result.append(data)


def run_strategy(num):
    from gm.model.storage import context
    # 用context传入回测次数参数
    context.num = num
    # context.result用以存储超参
    context.result = []
    '''
        strategy_id策略ID,由系统生成
        filename文件名,请与本文件名保持一致
        mode实时模式:MODE_LIVE回测模式:MODE_BACKTEST
        token绑定计算机的ID,可在系统设置-密钥管理中生成
        backtest_start_time回测开始时间
        backtest_end_time回测结束时间
        backtest_adjust股票复权方式不复权:ADJUST_NONE前复权:ADJUST_PREV后复权:ADJUST_POST
        backtest_initial_cash回测初始资金
        backtest_commission_ratio回测佣金比例
        backtest_slippage_ratio回测滑点比例
    '''
    run(strategy_id='859c3b0a-1765-11ec-acc4-d0509949eed8',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='{{token}}',
        backtest_start_time='2019-01-01 08:00:00',
        backtest_end_time='2020-12-31 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=1000000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)
    return context.result
    


if __name__ == '__main__':
    # 循环输入参数数值回测
    num = [[i] for i in range(1, 11)]

    a_list = []
    pool = multiprocessing.Pool(processes=10, maxtasksperchild=1)  # create 10 processes
    for i in range(len(num)):
        a_list.append(pool.apply_async(func=run_strategy, args=(num[i][0],)))
    pool.close()
    pool.join()
    info = []
    for pro in a_list:
        print('pro', pro.get()[0])
        info.append(pro.get()[0])
    print(info)
    info = pd.DataFrame(np.array(info), columns=['pnl_ratio', 'pnl_ratio_annual', 'sharp_ratio', 'max_drawdown', 'num'])
    info.to_csv('info.csv', index=False)
