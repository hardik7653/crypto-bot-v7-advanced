import json, traceback
from pathlib import Path
from fastapi import FastAPI
from bot.execution.exchange_connector import MockExchange
from bot.data.data_processor import add_indicators, make_supervised
from bot.models.model_manager import train_quick, load_model, predict
from bot.strategies.strategy import combine_signals
from bot.trading.trade_manager import log_trade, init_db
from bot.utils.logger import setup_logger

# Setup FastAPI
app = FastAPI()

log = setup_logger('main-v7')
HERE = Path(__file__).parent
cfg = json.loads((HERE/'config.json').read_text())

@app.get("/run_once")
def run_once():
    symbols = cfg.get('symbols', ['BTC/USDT', 'ETH/USDT'])
    exchange = MockExchange()
    dfs = []
    
    for s in symbols:
        df = exchange.fetch_ohlcv(s, timeframe=cfg.get('timeframe', '5m'), limit=300)
        df = add_indicators(df)
        dfs.append(df)
    
    if not dfs:
        return {"error": "No data fetched"}

    # Train quick model
    features = ['close', 'returns', 'atr', 'rsi', 'macd']
    try:
        model = load_model()
        if not model:
            train_quick(dfs, features)
            model = load_model()
    except Exception as e:
        log.exception('Train error %s', e)
        model = None

    reports = {}
    for s, df in zip(symbols, dfs):
        try:
            ml = predict(model, df) if model else None
            final = combine_signals(df, ml)
            latest = df.iloc[-1]
            price = float(latest['close'])
            atr = float(latest['atr'])
            sl = None
            tp = None
            if final != 'HOLD':
                sl = price - cfg.get('sl_atr_mult', 1.5) * atr if final == 'BUY' else price + cfg.get('sl_atr_mult', 1.5) * atr
                tp = price + cfg.get('tp_atr_mult', 3.0) * atr if final == 'BUY' else price - cfg.get('tp_atr_mult', 3.0) * atr
                log_trade(s, final, price, sl, tp, 0)
            reports[s] = {'signal': final, 'ml': ml, 'price': price, 'atr': atr, 'sl': sl, 'tp': tp}
            log.info('%s -> %s price=%.6f', s, final, price)
        except Exception as e:
            log.exception('Eval error %s', e)
            reports[s] = {'error': str(e)}

    (HERE/'reports'/'v7_multi_report.json').write_text(json.dumps(reports, indent=2))
    return reports

if __name__ == '__main__':
    try:
        init_db()
        r = run_once()
        print('Done. Report at reports/v7_multi_report.json')
        print(r)
    except Exception:
        traceback.print_exc()
