import sqlite3, re, datetime as dt, pandas as pd

def connect(path):
    con=sqlite3.connect(path); con.row_factory=sqlite3.Row; return con
def init_db(path):
    con=connect(path)
    con.execute('CREATE TABLE IF NOT EXISTS samples(sample_id TEXT PRIMARY KEY, project TEXT, sample_type TEXT, owner TEXT, status TEXT, created_at TEXT, folder_name TEXT)')
    con.execute('CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, action TEXT, sample_id TEXT, details TEXT)')
    con.commit(); con.close()
def slug(s): return re.sub(r'[^A-Za-z0-9._-]+','-',str(s).strip()).strip('-')
def validate(df,required):
    issues=[]
    for c in required:
        if c not in df: issues.append({'severity':'error','row':None,'issue':f'missing column {c}'})
        elif df[c].isna().any(): issues.append({'severity':'error','row':None,'issue':f'{c} contains blanks'})
    if 'sample_id' in df:
        for idx in df.index[df.sample_id.duplicated(keep=False)]: issues.append({'severity':'error','row':int(idx)+2,'issue':'duplicate sample_id'})
    return pd.DataFrame(issues)
def import_csv(path,df,required):
    issues=validate(df,required)
    if len(issues) and (issues.severity=='error').any(): return issues
    init_db(path); con=connect(path); now=dt.datetime.utcnow().isoformat()
    for _,r in df.iterrows():
        folder=f"{slug(r['project'])}/{slug(r['sample_id'])}_{slug(r['sample_type'])}"
        con.execute('INSERT OR REPLACE INTO samples VALUES(?,?,?,?,?,?,?)',(r.sample_id,r.project,r.sample_type,r.owner,r.status,now,folder))
        con.execute('INSERT INTO audit(ts,action,sample_id,details) VALUES(?,?,?,?)',(now,'import',r.sample_id,folder))
    con.commit(); con.close(); return issues
def list_samples(path): init_db(path); return pd.read_sql_query('SELECT * FROM samples ORDER BY project,sample_id',connect(path))
def update_status(path,sample_id,status):
    con=connect(path); now=dt.datetime.utcnow().isoformat(); con.execute('UPDATE samples SET status=? WHERE sample_id=?',(status,sample_id)); con.execute('INSERT INTO audit(ts,action,sample_id,details) VALUES(?,?,?,?)',(now,'status_change',sample_id,status)); con.commit(); con.close()
def audit_log(path): init_db(path); return pd.read_sql_query('SELECT * FROM audit ORDER BY id DESC',connect(path))
