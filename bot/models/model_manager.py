
import os, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
MODEL_FILE = os.path.join(os.path.dirname(__file__),'model_v7.joblib')
def train_quick(dfs, features):
    import pandas as pd
    Xs=[]; ys=[]
    for df in dfs:
        X,y,fe = __import__('bot.data.data_processor', fromlist=['']).make_supervised(df)
        Xs.append(X); ys.append(y)
    X_all = pd.concat(Xs)
    y_all = pd.concat(ys)
    y_bin = (y_all=='BUY').astype(int)
    scaler = StandardScaler()
    Xs_scaled = scaler.fit_transform(X_all[features].values)
    clf = RandomForestClassifier(n_estimators=30, random_state=42, class_weight='balanced', n_jobs=1)
    clf.fit(Xs_scaled, y_bin.values)
    model = {'scaler':scaler,'model':clf,'features':features}
    joblib.dump(model, MODEL_FILE)
    return MODEL_FILE
def load_model():
    if os.path.exists(MODEL_FILE):
        try:
            return joblib.load(MODEL_FILE)
        except:
            return None
    return None
def predict(model, df):
    feats = model['features']
    X = df[feats].iloc[[-1]].values
    Xs = model['scaler'].transform(X)
    proba = float(model['model'].predict_proba(Xs)[:,1][0])
    if proba>0.6: return {'signal':'BUY','conf':proba}
    if proba<0.4: return {'signal':'SELL','conf':1-proba}
    return {'signal':'HOLD','conf':abs(proba-0.5)*2}
