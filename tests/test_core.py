import pandas as pd
from src.core import validate,slug

def test_slug(): assert slug('Project A / 1')=='Project-A-1'
def test_validate_duplicate():
    df=pd.DataFrame({'sample_id':['x','x'],'project':['p','p'],'sample_type':['dna','dna'],'owner':['a','a'],'status':['new','new']})
    assert len(validate(df,['sample_id','project','sample_type','owner','status']))==2
