import json
from Moment import Moment
with open('/home/zhouh/下载/merge_json.json', 'r') as f1:
    data_new = json.load(f1)
event = data_new['events']
moments = event['moments']
Id = []
for i in range(len(moments)):
    moment = Moment(moments[i])
    player = [j.id for j in moment.players]
    Id.append(sorted(player))
total = 0
change_pos = []
for i in range(1,len(Id)):
    if Id[i] != Id[i-1]:
        total += 1
        change_pos.append(i)
#print(total)
#print(change_pos)
#for i in range(len(moments)):
#    moment = Moment(moments[i])
