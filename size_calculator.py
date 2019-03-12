import pandas as pd
import numpy as np
import math

current_risk = 0.02
capital = 170000

#df = pd.read_csv('day_data')

def EMA(df, column="Day Diff", period=5):

    ema = round(df[column].ewm(span=period, min_periods=period - 1).mean(), 1).shift(+1)
    return df.join(ema.to_frame('EMA'+ str(period)))

def BB(df):
    bb = df['Open'] < df['Close']
    return df.join(bb.to_frame('BB'))

def Trend(df):
    trend = df.BB
    if trend == True:
        trend_val = round(df['Close'] - df['Low'], 1)
    else:
        trend_val = round(df['High'] - df['Close'], 1)
    return df.join(trend_val.to_frame('Trend'))

df = pd.read_csv('C:/Code/Robex/Q1_demo/Kiwoom/1D_data_GCM17.csv')
print(df)
df['Day Diff'] = round(abs(df['High'] - df['Low']), 1)
df = EMA(df)
df = BB(df)
df['Trend'] = np.where(df['BB'] == True, df['Close'] - df['Low'], df['High'] - df['Close'])
df['Trend'] = round(df['Trend'], 1)
df['Rate %'] = round((df['Trend']/ df['Day Diff']) , 3)
df['N'] = round(((4/5)*df['EMA5']) + ((1/5)*df['Day Diff']*df['Rate %']), 1)
df['Unit'] = np.floor((capital*current_risk)/(df['N']*1/0.1*10))
df['Capital'] = capital
df['Risk %'] = current_risk

print(df)
#df = pd.DataFrame.replace(df['BB'], True, "Bull")
#df = pd.DataFrame.replace(df['BB'], False, "Bear")

df.to_csv('size_cal_1D_GCM17.csv')


