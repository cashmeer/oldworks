import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import *
from datetime import *
import re

#df = pd.read_csv('C:/Code/Robex/Q1_demo/Kiwoom/300Tick_data_GCM17.csv')
df = pd.read_csv('300Tick_data_GCM17.csv')
print(df)
print(df.dtypes)

def TRIX(df, n):
    EX1 = pd.DataFrame.ewm(df['close'], span = n, min_periods = n - 1).mean()
    EX2 = EX1.ewm(span = n, min_periods = n - 1).mean()
    EX3 = EX2.ewm(EX2, span = n, min_periods = n - 1).mean()
    i = 0
    ROC_l = [0]
    while i + 1 <= df.index[-1]:
        ROC = (EX3[i + 1] - EX3[i]) / EX3[i]
        ROC_l.append(ROC)
        i = i + 1
    Trix = pd.Series(ROC_l)
    return Trix

df['datetime'] = pd.to_datetime(df['datetime'])#,  format='%Y-%m-%d %H:%M:%S')

df['Date'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d'))
df['Time'] = df['datetime'].apply(lambda x: x.strftime('%H%M%S'))

trix_val = 1
df['Trix_' + str(trix_val)] = TRIX(df, trix_val)
df['Trix_shift_' + str(trix_val)] = TRIX(df, trix_val).shift(1)
print(df)

print(df)
print(df.dtypes)

time_list = df['Time'].tolist()
high_list = df['high'].tolist()
low_list = df['low'].tolist()
open_list = df['open'].tolist()
close_list = df['close'].tolist()
trix_list = df['Trix_' + str(trix_val)].tolist()
trix_shift_list = df['Trix_shift_' + str(trix_val)].tolist()

print(trix_list)
print(trix_shift_list)

next_max = []
next_min = []
day_medi = []
#cross_up = []
#cross_down = []
marketenter = []
buyorsell = []
def dayhigh():
    next_max_val = 0
    #open = 0
    for t, h in zip(time_list, high_list):
        if t == '070000':
            open = h
            next_max.append(open)
            next_max_val = h
        else:
            #print(h, next_max_val)
            #open = float(max(h, next_max[-1]))
            next_max_val = float(max(h, next_max_val))
            next_max.append(next_max_val)
            #next_max.append(open)
    print(next_max)

def daylow():
    next_min_val = 0
    #open = 0
    for t, l in zip(time_list, low_list):
        if t == '070000':
            open = l
            next_min.append(open)
            next_min_val = l
        else:
            #print(l, next_min_val)
            #open = float(max(h, next_max[-1]))
            next_min_val = float(min(l,next_min_val, key=lambda x: (x==0, x)))
            next_min.append(next_min_val)
            #next_max.append(open)
    print(next_min)

def daymedi():
    for dh, dl in zip(next_max,next_min):
        day_medi_val = (dh + dl) / 2
        day_medi.append(day_medi_val)
    print(day_medi)

def CrossDown(A, B):
    if A > B and A[1] <= B[1]:
        return False
    else:
        return True

def entermarket():
    b_count = 0
    s_count = 0
    for o, dm, t1, c, ts in zip(open_list, day_medi, trix_list, close_list, trix_shift_list):
        if o >= dm  and t1 >= 0 and ts <= 0:
            b_count = b_count + 1
            s_count = 0
            if b_count == 1:
                marketenter.append(c)
                buyorsell.append(str('buy'))
            else:
                marketenter.append(int(0))
                buyorsell.append(int(0))
        elif o <= dm and t1 <= 0 and ts >= 0:
            s_count = s_count + 1
            b_count = 0
            if s_count == 1:
                marketenter.append(c)
                buyorsell.append(str('sell'))
            else:
                marketenter.append(int(0))
                buyorsell.append(int(0))
        else:
            marketenter.append(int(0))
            buyorsell.append(int(0))
    print(buyorsell)
    print(marketenter)

dayhigh()
daylow()
daymedi()
entermarket()



#day_m = round((next_max + next_min) / 2, 1)
#print(day_m)
new_df = pd.DataFrame({
    'datetime' : df['datetime'],
    #'Time' : time_list,
    #'high' : high_list,
    'day_h': next_max,
    #'low'  : low_list,
    'day_l': next_min,
    'day_m' : day_medi,
    'trix1': trix_list,
    'b&s': buyorsell,
    '@price': marketenter
    }, columns= ['datetime', 'day_h', 'day_l', 'day_m','trix1','b&s', '@price'])

print(new_df)

result = pd.merge_asof(df, new_df, on='datetime')
#result['day_m'] = round((result['day_h'] + result['day_l']) / 2, 1)

#df = pd.DataFrame(result, columns=['datetime', 'open', 'high', 'low', 'close', 'day_h', 'day_l', 'day_m'])
#trix_val = 1
#df['Trix_' + str(trix_val)] = TRIX(df, trix_val)
#df['CU'] = df.where(df['open'] >= df['day_m'], df['close'], False) #& df['Trix_' + str(trix_val)] > 0
#print(df)
#print(df.dtypes)
#df.to_csv("0_df_opti_gcm17_300_data.csv")
print(result)
result.to_csv("entry_price_300Tick_GCM17.csv", )

