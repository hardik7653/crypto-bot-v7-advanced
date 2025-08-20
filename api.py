
from fastapi import FastAPI
import json, os
app = FastAPI()
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/signals')
def signals():
    p = 'reports/v7_multi_report.json'
    if os.path.exists(p): return json.loads(open(p).read())
    return {'status':'no_report'}
