from Constant import Constant
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Polygon
import score_info
import numpy as np
home_total_aver_velocity = score_info.home_total_aver_velocity
visitor_total_aver_velocity = score_info.visitor_total_aver_velocity

attack_area = score_info.attack_area
defend_area = score_info.defend_area
defend_area_not_score = score_info.defend_area_not_score
attack_area_not_score = score_info.attack_area_not_score
visitor_defend_area = score_info.visitor_defend_area
visitor_defend_area_not_score = score_info.visitor_defend_area_not_score
visitor_attack_area = score_info.visitor_attack_area
visitor_attack_area_not_score = score_info.visitor_attack_area_not_score

home_total_player_pos = score_info.home_total_player_pos
home_point_pos = score_info.home_point_pos
visitor_total_player_pos = score_info.visitor_total_player_pos
visitor_point_pos = score_info.visitor_point_pos

######################################## home team ###############################
def show_shooting_position(team_point_pos):
    for i in range(len(team_point_pos)):
        if team_point_pos[i][0] > 47:
            team_point_pos[i][0] = team_point_pos[i][0] - 47
            if team_point_pos[i][0] > 35:
                team_point_pos[i][0] = team_point_pos[i][0] - 10

    ax = plt.axes(xlim=(Constant.X_MIN,
                  Constant.X_MAX),
                  ylim=(Constant.Y_MIN,
                        Constant.Y_MAX))
    ax.axis("off")
    fig = plt.gcf()

    pos_circles = [plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE) for _ in range(len(team_point_pos))]

    for j, circle in enumerate(pos_circles):
        circle.center = team_point_pos[j][0], team_point_pos[j][1]
    for circle in pos_circles:
        ax.add_patch(circle)
    court = plt.imread("court.png")
    plt.imshow(court, zorder=0, extent=[Constant.X_MIN, Constant.X_MAX - Constant.DIFF,
               Constant.Y_MAX, Constant.Y_MIN])
    plt.show()


################################### velocity  ######################
def show_velocity(velocity):
    plt.plot(velocity)
    plt.xlabel("Attack Time")
    plt.ylabel("Average Velocity feet/s")
    #plt.title(team_name)
    plt.show()
################################### spacing area ###################
def show_spacing_area(defend_area_not_score, attack_area_not_score):
    plt.plot(defend_area_not_score, color = 'b',label = "defend")
    plt.plot(attack_area_not_score, color = 'r', label = "attack")
    plt.plot(defend_area_not_score, color = 'b')
    plt.plot([np.mean(attack_area_not_score)] * len(attack_area_not_score), color = 'r')
    plt.plot([np.mean(defend_area_not_score)] * len(defend_area_not_score), color = 'b')
    plt.xlabel("Attack Time")
    plt.ylabel("Spacing area sqf")
    
    plt.show()
###############################################################
show_spacing_area(defend_area,attack_area)
show_spacing_area(defend_area_not_score, attack_area_not_score)
show_spacing_area(visitor_defend_area,visitor_attack_area)
show_spacing_area(visitor_defend_area_not_score, visitor_attack_area_not_score)
###############################################################
show_shooting_position(home_point_pos)
show_shooting_position(visitor_point_pos)

show_velocity(home_total_aver_velocity)
show_velocity(visitor_total_aver_velocity)

print("attack area when visitor team offense")
print("attack area",np.mean(visitor_attack_area))
print("defend area",np.mean(visitor_defend_area))
print("attack area when home team offense")
print("attack area",np.mean(attack_area))
print("defend area",np.mean(defend_area))

