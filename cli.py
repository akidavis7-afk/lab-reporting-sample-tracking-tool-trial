import argparse,pandas as pd
from pathlib import Path
from src.core import init_db,import_csv,list_samples,audit_log
p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
a=sub.add_parser('init'); a.add_argument('--db',required=True)
a=sub.add_parser('import'); a.add_argument('--db',required=True); a.add_argument('--csv',required=True)
a=sub.add_parser('report'); a.add_argument('--db',required=True); a.add_argument('--output',default='outputs')
x=p.parse_args()
if x.cmd=='init': init_db(x.db)
elif x.cmd=='import': print(import_csv(x.db,pd.read_csv(x.csv),['sample_id','project','sample_type','owner','status']))
else:
 out=Path(x.output); out.mkdir(exist_ok=True); list_samples(x.db).to_csv(out/'samples.csv',index=False); audit_log(x.db).to_csv(out/'audit.csv',index=False); print(out)
