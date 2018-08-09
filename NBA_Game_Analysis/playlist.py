import json
with open('/home/zhouh/下载/merge_json.json', 'r') as f1:
    merge = json.load(f1)

home_team = merge['events']['home']['players']
visitor_team = merge['events']['visitor']['players']
#print(home_team)
playlist = {}
for player in home_team:
    playlist[player['playerid']] = player['lastname']

visitorplaylist = {}
for player in visitor_team:
    visitorplaylist[player['playerid']] = player['lastname']
#print(playlist)
home_total_player_pos = {}
for n in range(len(home_team)):
    home_total_player_pos[home_team[n]['playerid']] = []

visitor_total_player_pos = {}
for n in range(len(visitor_team)):
    visitor_total_player_pos[visitor_team[n]['playerid']] = []
#print(total)
