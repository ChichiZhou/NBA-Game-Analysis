import json
import pandas as pd
import numpy as np
from Moment import Moment
import playlist
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

home_total_player_pos = playlist.home_total_player_pos 
visitor_total_player_pos = playlist.visitor_total_player_pos
visitorplaylist = playlist.visitorplaylist  
playlist = playlist.playlist  



data = pd.read_csv('/home/zhouh/下载/0021500492.csv')
data['Time'] = data.PCTIMESTRING.str.split(':',expand = True)[0].astype(int)*60 + data.PCTIMESTRING.str.split(':',expand = True)[1].astype(int)

data_new = data[['PERIOD','Time','HOMEDESCRIPTION', 'VISITORDESCRIPTION', 'SCORE', 'SCOREMARGIN']]
#########################   home team offense without score ###############
not_score = data_new[data_new['SCORE'].isna()]
home_not_score = not_score[not_score['HOMEDESCRIPTION'].notna()]
home_not_score = np.array(home_not_score)

########################    visitor team offense without score  ##############
visitor_not_score = not_score[not_score['VISITORDESCRIPTION'].notna()]
visitor_not_score = np.array(visitor_not_score)

##########################


a = list(data_new[data_new['SCORE'].isna()].index)
data_new.drop(a)
data_new = data_new.drop(a)  
data_new.loc[data_new['SCOREMARGIN'] == 'TIE', 'SCOREMARGIN'] = 0   
data_new['SCOREMARGIN'] = data_new['SCOREMARGIN'].astype(int)


###############################  home team score moments ####################################
home = data_new[data_new['HOMEDESCRIPTION'].notna()]   
home = np.array(home)

############################### visitor team score moments ########################################
visitor = data_new[data_new['VISITORDESCRIPTION'].notna()]
visitor = np.array(visitor)
###############################  get scorer for home team #####################
home_scorer = []
visitor_scorer = []


for i in range(len(home)):
    home_scorer.append(str.split(home[i][2])[0])
for i in range(len(visitor)):
    visitor_scorer.append(str.split(visitor[i][3])[0])


##########################################################################################


with open('/home/zhouh/下载/merge_json.json', 'r') as f1:
    merge = json.load(f1)

home_score_point = []    
home_not_score_point = [] 
visitor_score_point = []
visitor_not_score_point = []
home_aver_pos = []   
home_aver_pos_val = 0
visitor_aver_pos = []
visitor_aver_pos_val = 0

################# get average position ##################
for moment in merge['events']['moments']:
    moment = Moment(moment)
    for n in range(5):
        home_aver_pos_val += moment.players[n].x
    home_aver_pos_val /= 5
    home_aver_pos.append(home_aver_pos_val)
    for m in range(5, 10):
        visitor_aver_pos_val += moment.players[m].x
    visitor_aver_pos_val /= 5
    visitor_aver_pos.append(visitor_aver_pos_val)



################    home team score round  ##################################
for j in range(len(home)):
    for i in range(len(merge['events']['moments'])):
        if (merge['events']['moments'][i][0] == home[j][0]) and (int(merge['events']['moments'][i][2]) == home[j][1]):

            stack = []
            if home[j][0] < 3:
                while home_aver_pos[i] < 47:
                    stack.append(merge['events']['moments'][i])
                    i -= 1
            else:
                while home_aver_pos[i] > 47:
                    stack.append(merge['events']['moments'][i])
                    i -= 1
            stack.reverse()
            if len(stack) > 0:  
                home_score_point.append(stack)  
            break
    continue
###############################   home team without score round  ###############################

for j in range(len(home_not_score)):

    for i in range(len(merge['events']['moments'])):
        if (merge['events']['moments'][i][0] == home_not_score[j][0]) and (int(merge['events']['moments'][i][2]) == home_not_score[j][1]):

            stack = []
            if home_not_score[j][0] < 3:
               while home_aver_pos[i] < 47:
                    stack.append(merge['events']['moments'][i])
                    i -= 1
                    if i < 0:
                        break
            else:
                while home_aver_pos[i] > 47:
                    stack.append(merge['events']['moments'][i])
                    i -= 1
            stack.reverse()
            if len(stack) > 0:  
                home_not_score_point.append(stack)  
            break
    continue
print("***visitor*******")
print(len(visitor))
#######################################################################

############################## visitor team score round #################

for j in range(len(visitor)):

    for i in range(len(merge['events']['moments'])):
        if (merge['events']['moments'][i][0] == visitor[j][0]) and (int(merge['events']['moments'][i][2]) == visitor[j][1]):
            stack = []
            if visitor[j][0] < 3:
                while visitor_aver_pos[i] > 47:
                    stack.append(merge['events']['moments'][i])
                    i -= 1
            else:
                while visitor_aver_pos[i] > 47:
                    stack.append(merge['events']['moments'][i])
                    i -= 1
            stack.reverse()
            if len(stack) > 0:  
                visitor_score_point.append(stack)  
            break
    continue

###############################  visitor team offense without score ########################
for j in range(len(visitor_not_score)):

    for i in range(len(merge['events']['moments'])):
        if (merge['events']['moments'][i][0] == visitor_not_score[j][0]) and (int(merge['events']['moments'][i][2]) == visitor_not_score[j][1]):
         
            stack = []
            if visitor_not_score[j][0] < 3:
                while visitor_aver_pos[i] > 47:
                    stack.append(merge['events']['moments'][i])
                    i -= 1
                    if i < 0:
                        break
            else:
                while visitor_aver_pos[i] < 47:
                    stack.append(merge['events']['moments'][i])
                    i -= 1
            stack.reverse()
            if len(stack) > 0:  
                visitor_not_score_point.append(stack)  
            break
    continue

        
################### home team offense velocity ##############################

home_total_aver_velocity = []
home_player_velocity = []
for i in range(len(home_score_point)):
    for player in range(1,6):
        x_distance = []
        y_distance = []
        time_distance = []
        for n in range(1, len(home_score_point[i])):
            x_distance.append(home_score_point[i][n][5][player][2] - home_score_point[i][n - 1][5][player][2])
            y_distance.append(home_score_point[i][n][5][player][3] - home_score_point[i][n - 1][5][player][3])
            time_distance.append(abs(home_score_point[i][n][2] - home_score_point[i][n - 1][2]))

        x_distance = np.array(x_distance) ** 2
        y_distance = np.array(y_distance) ** 2
        time_distance = np.array(time_distance)
        total_distance = (x_distance + y_distance) ** 0.5
        total_velocity = total_distance / time_distance
        home_player_velocity.append(total_velocity.mean())
    home_total_aver_velocity.append(np.mean(home_player_velocity))


################## visitor team offense velocity ####################
visitor_total_aver_velocity = []
visitor_player_velocity = []
for i in range(len(visitor_score_point)):
    for player in range(1,6):
        x_distance = []
        y_distance = []
        time_distance = []
        for n in range(1, len(visitor_score_point[i])):
            x_distance.append(visitor_score_point[i][n][5][player][2] - visitor_score_point[i][n - 1][5][player][2])
            y_distance.append(visitor_score_point[i][n][5][player][3] - visitor_score_point[i][n - 1][5][player][3])
            time_distance.append(abs(visitor_score_point[i][n][2] - visitor_score_point[i][n - 1][2]))

        x_distance = np.array(x_distance) ** 2
        y_distance = np.array(y_distance) ** 2
        time_distance = np.array(time_distance)
        total_distance = (x_distance + y_distance) ** 0.5
        total_velocity = total_distance / time_distance
        visitor_player_velocity.append(total_velocity.mean())
    visitor_total_aver_velocity.append(np.mean(visitor_player_velocity))


#print("velocity lenght", len(visitor_total_aver_velocity))
#print(visitor_total_aver_velocity)
#print("length of home_score_point", len(home_score_point))            

############### visitor team offense velocity #################################

################### home team score position  ################
home_point_pos = []

for j in range(len(home)):
    for i in range(len(merge['events']['moments'])):
        if (merge['events']['moments'][i][0] == home[j][0]) and (int(merge['events']['moments'][i][2]) == home[j][1]): 
            player_list = merge['events']['moments'][i- 1][5][1:]
            for n in range(5):
                if playlist[player_list[n][1]] == home_scorer[j]:
                    home_point_pos.append([player_list[n][2],player_list[n][3]])
                    home_total_player_pos[player_list[n][1]].append([player_list[n][2],player_list[n][3]])
            break

################## visitor team score position ######################
visitor_point_pos = []
for j in range(len(visitor)):
    for i in range(len(merge['events']['moments'])):
        if (merge['events']['moments'][i][0] == visitor[j][0]) and (int(merge['events']['moments'][i][2]) == visitor[j][1]):
            player_list = merge['events']['moments'][i][5][1:]
            for n in range(6, 10):
                if visitorplaylist[player_list[n][1]] == visitor_scorer[j]:
                    visitor_point_pos.append([player_list[n][2],player_list[n][3]])
                    visitor_total_player_pos[player_list[n][1]].append([player_list[n][2],player_list[n][3]])
            break


print("home points pos")
print(len(visitor_point_pos))

################### player score position ##########################
        
#print(total_player_pos)
#print(point_pos)
#player_list = home_score_point[0][-2][5][1:]
#for n in player_list:
#    print(n)
#print(len(home_score_point))
#print("*********")
#print(len(home_scorer))
#########################################################################################

############# get space area ###########################################
################### home team offense #######################
defend_area = []
defend_area_not_score = []
for i in range(len(home_score_point)):  
    area = []
    for j in range(len(home_score_point[i])):   
        x_pos = [move[2] for move in home_score_point[i][j][5][6:]]
        y_pos = [move[3] for move in home_score_point[i][j][5][6:]]
        xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
        area.append(ConvexHull(xy_pos).area)   
    defend_area.append(np.mean(area))

attack_area = []
for i in range(len(home_score_point)):  
    area = []
    for j in range(len(home_score_point[i])):   
        x_pos = [move[2] for move in home_score_point[i][j][5][1:6]]
        y_pos = [move[3] for move in home_score_point[i][j][5][1:6]]
        xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
        area.append(ConvexHull(xy_pos).area)   
    attack_area.append(np.mean(area))



attack_area_not_score = []

for i in range(len(home_not_score_point)):
    area = []
    for j in range(len(home_not_score_point[i])):
        x_pos = [move[2] for move in home_not_score_point[i][j][5][1:6]]
        y_pos = [move[3] for move in home_not_score_point[i][j][5][1:6]]
        xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
        area.append(ConvexHull(xy_pos).area)
    attack_area_not_score.append(np.mean(area))

for i in range(len(home_not_score_point)):
    area = []
    for j in range(len(home_not_score_point[i])):
        x_pos = [move[2] for move in home_not_score_point[i][j][5][6:]]
        y_pos = [move[3] for move in home_not_score_point[i][j][5][6:]]
        xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
        area.append(ConvexHull(xy_pos).area)
    defend_area_not_score.append(np.mean(area))




plt.show()
############# 主队投球的那一刹那，客队防守区域 ##########################
final_defend_area = []
for i in range(len(home_score_point)):  ### 第i次得分 ###
    x_pos = [move[2] for move in home_score_point[i][-2][5][6:]]
    y_pos = [move[3] for move in home_score_point[i][-2][5][6:]]
    xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
    final_defend_area.append(ConvexHull(xy_pos).area)
    
#plt.plot(defend_area, color = 'b', label = 'average defend area')
#plt.plot([np.mean(defend_area)]*len(defend_area), color = 'b')
#plt.plot(final_defend_area, color = 'g', label = 'defend area before shoot')
#plt.plot([np.mean(final_defend_area)]*len(defend_area), color = 'g')
#plt.legend(loc = (0,0))
#plt.show()
#plt.plot(attack_area_not_score, color = 'r')
#plt.plot(defend_area_not_score, color = 'b')
#plt.show()

#print("******主队进球时进攻面积与防守面积******")
#print(np.mean(attack_area))
#print(np.mean(defend_area))
#print("******主队没进球时进攻面积与防守面积******")
#print(np.mean(attack_area_not_score))
#print(np.mean(defend_area_not_score))

#plt.plot(defend_area_not_score, color = 'b',label = "CHA")
#plt.plot(attack_area_not_score, color = 'r', label = "TOR")
#plt.plot(defend_area_not_score, color = 'b')
#plt.plot([np.mean(attack_area_not_score)] * len(attack_area_not_score), color = 'r')
#plt.plot([np.mean(defend_area_not_score)] * len(defend_area_not_score), color = 'b')
#plt.xlabel("Attack Time")
#plt.ylabel("Spacing area sqf")
#plt.title("TOR Not Score")
#plt.show()



######################## visitor team offense #########################
visitor_defend_area = []
visitor_defend_area_not_score = []
for i in range(len(visitor_score_point)):  
    area = []
    for j in range(len(visitor_score_point[i])):   
        x_pos = [move[2] for move in visitor_score_point[i][j][5][1:6]]
        y_pos = [move[3] for move in visitor_score_point[i][j][5][1:6]]
        xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
        area.append(ConvexHull(xy_pos).area)   
    visitor_defend_area.append(np.mean(area))

for i in range(len(visitor_not_score_point)):
    area = []
    for j in range(len(visitor_not_score_point[i])):
        x_pos = [move[2] for move in visitor_not_score_point[i][j][5][1:6]]
        y_pos = [move[3] for move in visitor_not_score_point[i][j][5][1:6]]
        xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
        area.append(ConvexHull(xy_pos).area)
    visitor_defend_area_not_score.append(np.mean(area))

visitor_attack_area_not_score = []
for i in range(len(visitor_not_score_point)):
    area = []
    for j in range(len(visitor_not_score_point[i])):
        x_pos = [move[2] for move in visitor_not_score_point[i][j][5][6:]]
        y_pos = [move[3] for move in visitor_not_score_point[i][j][5][6:]]
        xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
        area.append(ConvexHull(xy_pos).area)
    visitor_attack_area_not_score.append(np.mean(area))






visitor_attack_area = []
for i in range(len(visitor_score_point)):  
    area = []
    for j in range(len(visitor_score_point[i])):   
        x_pos = [move[2] for move in visitor_score_point[i][j][5][6:]]
        y_pos = [move[3] for move in visitor_score_point[i][j][5][6:]]
        xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
        area.append(ConvexHull(xy_pos).area)   
    visitor_attack_area.append(np.mean(area))




visitor_final_defend_area = []
for i in range(len(visitor_score_point)):  
    x_pos = [move[2] for move in visitor_score_point[i][-2][5][1:5]]
    y_pos = [move[3] for move in visitor_score_point[i][-2][5][1:5]]
    xy_pos = np.column_stack((np.array(x_pos), np.array(y_pos)))
    visitor_final_defend_area.append(ConvexHull(xy_pos).area)





########################################
#print("******客队进球时进攻面积与防守面积******")
#print(np.mean(visitor_attack_area))
#print(np.mean(visitor_defend_area))
#print("******客队没进球时进攻面积与防守面积******")
#print(np.mean(visitor_attack_area_not_score))
#print(np.mean(visitor_defend_area_not_score))

#plt.plot(visitor_defend_area_not_score, color = 'b',label = "CHA")
#plt.plot(visitor_attack_area_not_score, color = 'r', label = "TOR")
#plt.plot(visitor_not_defend_area, color = 'b')
#plt.plot([np.mean(visitor_attack_area_not_score)] * len(visitor_attack_area_not_score), color = 'r')
#plt.plot([np.mean(visitor_defend_area_not_score)] * len(visitor_defend_area_not_score), color = 'b')
#plt.xlabel("Attack Time")
#plt.ylabel("Spacing area sqf")
#plt.title("CHA Not Score")
#plt.show()

#plt.plot(visitor_defend_area, color = 'r', label = 'average defend area')
#plt.plot([np.mean(visitor_defend_area)]*len(visitor_defend_area), color = 'r')
#plt.plot(visitor_final_defend_area, color = 'g', label = 'defend area before shoot')
#plt.plot([np.mean(visitor_final_defend_area)]*len(visitor_defend_area), color = 'g')
#plt.legend(loc = (0,0))
#plt.show()


merge['events']['moments'] = home_score_point   
#print(home_score_point[2])
#for i in range(20):
#    print(home_score_point[i])
#print("score")
#print(np.mean(visitor_defend_area))
#print("***********")
#print("not score")
#print(np.mean(visitor_defend_area_not_score))
with open('/home/zhouh/下载/merge_score_data.json', 'w') as f:
    d = json.dumps(merge)
    f.write(d)



