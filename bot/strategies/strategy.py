
def combine_signals(df, ml_sig=None):
    last = df.iloc[-1]
    # trend filter: ema12 > ema26
    trend = last['ema12'] > last['ema26']
    if ml_sig and ml_sig.get('conf',0) > 0.65 and trend:
        return ml_sig['signal']
    if last['rsi'] < 30:
        return 'BUY'
    if last['rsi'] > 70:
        return 'SELL'
    return 'HOLD'
