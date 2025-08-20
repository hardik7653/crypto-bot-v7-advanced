
import pandas as pd, numpy as np
def add_indicators(df):
    df = df.copy()
    df['returns'] = df['close'].pct_change().fillna(0)
    df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ema12'] - df['ema26']
    tr1 = df['high'] - df['low']
    tr2 = (df['high'] - df['close'].shift(1)).abs()
    tr3 = (df['low'] - df['close'].shift(1)).abs()
    df['tr'] = pd.concat([tr1,tr2,tr3], axis=1).max(axis=1)
    df['atr'] = df['tr'].rolling(14, min_periods=1).mean().fillna(0)
    delta = df['close'].diff().fillna(0)
    up = delta.clip(lower=0).rolling(14, min_periods=1).mean()
    down = -delta.clip(upper=0).rolling(14, min_periods=1).mean()
    rs = up/(down+1e-9)
    df['rsi'] = 100 - (100/(1+rs))
    return df
def make_supervised(df, horizon=3):
    df2 = df.copy().reset_index(drop=True)
    df2['target_ret']=df2['close'].shift(-horizon)/df2['close'] - 1.0
    df2['target']='HOLD'
    df2.loc[df2['target_ret']>0.002,'target']='BUY'
    df2.loc[df2['target_ret']<-0.002,'target']='SELL'
    feats=['close','returns','atr','rsi','macd']
    X=df2[feats].iloc[:-horizon].copy()
    y=df2['target'].iloc[:-horizon].copy()
    return X,y,feats
