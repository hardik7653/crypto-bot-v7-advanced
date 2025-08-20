
def simple_backtest(df, signals):
    pnl=0.0; trades=[]
    for i,sig in enumerate(signals):
        if i+1>=len(df): break
        entry=df['close'].iloc[i]; exitp=df['close'].iloc[i+1]
        ret=(exitp/entry -1.0)
        if sig=='BUY': pnl+=ret
        elif sig=='SELL': pnl-=ret
        trades.append({'idx':i,'sig':sig,'entry':entry,'exit':exitp,'ret':ret})
    return {'n_trades':len(trades),'pnl':pnl,'trades':trades}
