from Constant import Constant
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Polygon
import score_info

home_total_player_pos = score_info.home_total_player_pos
home_point_pos = score_info.home_point_pos
visitor_total_player_pos = score_info.visitor_total_player_pos
visitor_point_pos = score_info.visitor_point_pos
####################  初步探查还算可以，一些异常点属于数据本身的问题  ############
point_pos = [[5.4819, 26.61151], [5.4819, 26.61151], [12.55304, 47.6258], [14.08342, 24.52261], [9.72169, 0.93687], [4.10857, 45.81925], [40.51824, 10.49626], [3.08232, 18.56255], [32.21336, 18.98199], [16.4309, 32.41676], [33.83681, 36.39406], [5.87304, 27.38163], [4.1807, 26.96437], [23.50427, 41.50172], [31.14472, 26.60948], [7.02621, 36.37896], [33.59712, 16.77272], [5.28737, 25.61552], [29.39791, 18.50395], [6.94405, 26.70417], [6.94405, 26.70417], [4.68089, 17.27821], [4.68089, 17.27821], [28.16906, 23.93242], [28.16906, 23.93242], [7.84223, 49.14907], [86.9652, 33.69428], [80.8213, 21.09109], [72.8469, 24.06299], [63.94064, 47.23585], [52.709, 22.99957], [87.88625, 19.45848], [87.88625, 19.45848], [62.74451, 29.43069], [64.84221, 36.68441], [89.33944, 27.17581], [89.33944, 27.17581], [71.41858, 8.09987], [85.64444, 23.00268], [72.19322, 5.1234], [97.39797, 21.86806], [60.02502, 1.54874], [91.30439, 25.32303], [46.25344, 24.5994], [84.86689, 1.29547], [83.60952, 1.55701], [83.60952, 1.55701]]


'''player_point_pos = [[12.91185, 47.556], [3.41436, 18.58697], [32.63017, 18.96499], [16.50074, 32.47723], [6.06249, 27.24565], [4.01941, 26.76983], [29.79109, 18.48264], [4.70828, 17.77677], [4.70828, 17.77677], [8.04494, 49.25196], [88.18429, 19.89532], [88.18429, 19.89532], [83.40888, 1.59129], [83.40888, 1.59129]]'''


######################################## 整个球队 #################################

for i in range(len(visitor_point_pos)):
    if visitor_point_pos[i][0] > 47:
        visitor_point_pos[i][0] = visitor_point_pos[i][0] - 47
        if visitor_point_pos[i][0] > 35:
            visitor_point_pos[i][0] = visitor_point_pos[i][0] - 10

ax = plt.axes(xlim=(Constant.X_MIN,
              Constant.X_MAX),
              ylim=(Constant.Y_MIN,
                    Constant.Y_MAX))
ax.axis("off")
fig = plt.gcf()

pos_circles = [plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE) for _ in range(len(visitor_point_pos))]

for j, circle in enumerate(pos_circles):
    circle.center = visitor_point_pos[j][0], visitor_point_pos[j][1]

for circle in pos_circles:
    ax.add_patch(circle)

court = plt.imread("court.png")
plt.imshow(court, zorder=0, extent=[Constant.X_MIN, Constant.X_MAX - Constant.DIFF,
           Constant.Y_MAX, Constant.Y_MIN])
plt.show()
################################### 某个球员 ######################
'''for i in range(len(visitor_point_pos)):
    if visitor_point_pos[i][0] > 47:
        visitor_point_pos[i][0] = visitor_point_pos[i][0] - 47
        if visitor_point_pos[i][0] > 35:
            visitor_point_pos[i][0] = visitor_point_pos[i][0] - 10

ax = plt.axes(xlim=(Constant.X_MIN,
              Constant.X_MAX),
              ylim=(Constant.Y_MIN,
                    Constant.Y_MAX))
ax.axis("off")
fig = plt.gcf()

pos_circles = [plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE) for _ in range(len(visitor_point_pos))]

for j, circle in enumerate(pos_circles):
    circle.center = visitor_point_pos[j][0], visitor_point_pos[j][1]

for circle in pos_circles:
    ax.add_patch(circle)

court = plt.imread("court.png")
plt.imshow(court, zorder=0, extent=[Constant.X_MIN, Constant.X_MAX - Constant.DIFF,
           Constant.Y_MAX, Constant.Y_MIN])
plt.show()'''
         
