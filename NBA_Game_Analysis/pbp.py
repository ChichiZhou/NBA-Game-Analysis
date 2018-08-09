import pandas as pd
import numpy as np

data = pd.read_csv('/home/zhouh/下载/0021500492.csv')
data.SCORE = data.SCORE.fillna(method = 'ffill').fillna('0-0')
data['Time'] = data.PCTIMESTRING.str.split(':',expand = True)[0].astype(int)*60 + data.PCTIMESTRING.str.split(':',expand = True)[1].astype(int)
data_new = data[['PERIOD','Time','SCORE']]

pbp_data = np.array(data_new)
#print(pbp_data)
