import json
import numpy as np
import pbp
import pandas as pd
with open('/home/zhouh/下载/0021500492.json', 'r') as load_f:
	data = json.load(load_f)
merge = {}
merge['gameid'] = data['gameid']
merge['gamedate'] = data['gamedate']
merge['events'] = {}
merge['events']['visitor'] = data['events'][0]['visitor']
merge['events']['home'] = data['events'][0]['home']
merge['events']['moments'] = []

for i in range(len(data['events'])):
	#merge['events']['moments'].extend(data['events'][i]['moments'])
	for j in range(len(data['events'][i]['moments'])):
		if len(merge['events']['moments']) == 0:
			merge['events']['moments'].append(data['events'][i]['moments'][j])
		else:
			if (merge['events']['moments'][-1][2] <= data['events'][i]['moments'][j][2]) and  (merge['events']['moments'][-1][0] == data['events'][i]['moments'][j][0]):
				continue
			else:
				if len(data['events'][i]['moments'][j][5]) < 11:
					continue
				if len(data['events'][i]['moments'][j]) > 0:
					merge['events']['moments'].append(data['events'][i]['moments'][j])
				else:
					continue

####  融合得分数据 ##############
pbp_data = pbp.pbp_data
merge['events']['moments'][0][4] = '0-0'

for i in range(len(merge['events']['moments'])):
    for j in range(len(pbp_data)):
        if (merge['events']['moments'][i][0] == pbp_data[j][0]) & (int(merge['events']['moments'][i][2]) == pbp_data[j][1]):
            merge['events']['moments'][i][4] = pbp_data[j][2]

for i in range(1, len(merge['events']['moments'])):
    if merge['events']['moments'][i][4]:
        continue
    else:
        merge['events']['moments'][i][4] = merge['events']['moments'][i - 1][4]

with open('/home/zhouh/下载/merge_json.json', 'w') as f:
	d = json.dumps(merge)
	f.write(d)

with open('/home/zhouh/下载/merge_json.json', 'r') as f1:
	data_new = json.load(f1)
for i in range(100):
    print(data_new['events']['moments'][i])

# 已经基本提取了信息, 并且融合了得分数据


