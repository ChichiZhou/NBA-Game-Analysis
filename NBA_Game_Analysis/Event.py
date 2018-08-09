from Constant import Constant
from Moment import Moment
from Team import Team
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Rectangle, Arc, Polygon
from scipy.spatial import ConvexHull
import numpy as np
import change

class Event:
    """A class for handling and showing events"""
    def __init__(self, event):
        moments = event['moments']
        self.moments = [Moment(moment) for moment in moments]
        home_players = event['home']['players']
        guest_players = event['visitor']['players']
        players = home_players + guest_players
        player_ids = [player['playerid'] for player in players]
        player_names = [" ".join([player['firstname'],
                        player['lastname']]) for player in players]
        player_jerseys = [player['jersey'] for player in players]
        values = list(zip(player_names, player_jerseys))
        # Example: 101108: ['Chris Paul', '3']
        self.player_ids_dict = dict(zip(player_ids, values))

    def update_radius(self, i, player_circles, ball_circle, annotations, clock_info,home_xy_pos, visitor_xy_pos, start):
        moment = self.moments[start + i]
        
        xy_home = [[0,0] for i in range(5)]
        xy_visitor = [[0,0] for i in range(5)]
        home = []
        visitor = []
        
        for n in range(10):
            if moment.players[n].team.name == 'TOR':
                home.append(n)
            else:
                visitor.append(n)
        
        #xy = [[0,0] for i in range(10)]
        for n in range(len(home)):
            xy_home[n][0] = moment.players[home[n]].x
            xy_home[n][1] = moment.players[home[n]].y
        home_xy_pos.set_xy(xy_home)
        
        for n in range(len(visitor)):
            xy_visitor[n][0] = moment.players[visitor[n]].x
            xy_visitor[n][1] = moment.players[visitor[n]].y
        visitor_xy_pos.set_xy(xy_visitor)

        for j, circle in enumerate(player_circles):
            circle.center = moment.players[j].x, moment.players[j].y   
            annotations[j].set_position(circle.center)       #  显示球员的编号
            #xy_pos[j][0] = moment.players[j].x
            #xy_pos[j][1] = moment.players[j].y
            ########### 在表下面显示比分 ############
            clock_test = 'Quarter {:d}\n {:02d}:{:02d}\n {:03.1f}\n {}'.format(
                         moment.quarter,
                         int(moment.game_clock) % 3600 // 60,
                         int(moment.game_clock) % 60,
                         moment.shot_clock,
                         moment.score
                         )
            clock_info.set_text(clock_test)
            #score_info.set_text(moment.score)
        ball_circle.center = moment.ball.x, moment.ball.y
        ball_circle.radius = moment.ball.radius / Constant.NORMALIZATION_COEF
        return player_circles

    def show(self, start, end):
        # Leave some space for inbound passes
        ax = plt.axes(xlim=(Constant.X_MIN,
                            Constant.X_MAX),
                      ylim=(Constant.Y_MIN,
                            Constant.Y_MAX))
        ax.axis('off')
        fig = plt.gcf()
        ax.grid(False)  # Remove grid
        start_moment = self.moments[start]
        player_dict = self.player_ids_dict
        ##########################################
        home_xy_pos = Polygon(xy = [[0,0] for i in range(5)], alpha = 0.3, color = 'r')
        visitor_xy_pos = Polygon(xy = [[0,0] for i in range(5)], alpha = 0.3, color = 'b')
        ##########################################
        clock_info = ax.annotate('', xy=[Constant.X_CENTER, Constant.Y_CENTER],
                                 color='black', horizontalalignment='center',
                                   verticalalignment='center')
        #score_info = ax.annotate('', xy=[Constant.X_CENTER + 10, Constant.Y_CENTER + 10],
        #                         color='black', horizontalalignment='center',
        #                          verticalalignment='center')
        annotations = [ax.annotate(self.player_ids_dict[player.id][1], xy=[0, 0], color='w',
                                   horizontalalignment='center',
                                   verticalalignment='center', fontweight='bold')
                       for player in start_moment.players]
        
        ######### 为显示球员编号及姓名做准备 ####################
        sorted_players = sorted(start_moment.players, key=lambda player: player.team.id)
        
        home_player = sorted_players[0]
        guest_player = sorted_players[5]
        column_labels = tuple([home_player.team.name, guest_player.team.name])
        column_colours = tuple([home_player.team.color, guest_player.team.color])
        cell_colours = [column_colours for _ in range(5)]
        
        home_players = [' #'.join([player_dict[player.id][0], player_dict[player.id][1]]) for player in sorted_players[:5]]
        guest_players = [' #'.join([player_dict[player.id][0], player_dict[player.id][1]]) for player in sorted_players[5:]]
        players_data = list(zip(home_players, guest_players))
        ############################################################
  
        ########## 显示球员编号及姓名 #####################
        table = plt.table(cellText=players_data,
                              colLabels=column_labels,
                              colColours=column_colours,
                              colWidths=[Constant.COL_WIDTH, Constant.COL_WIDTH],
                              loc='bottom',
                              cellColours=cell_colours,
                              fontsize=Constant.FONTSIZE,
                              cellLoc='center')
        table.scale(1, Constant.SCALE)
        table_cells = table.properties()['child_artists']
        for cell in table_cells:
            cell._text.set_color('white')
        #######################################
        
        player_circles = [plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE, color=player.color)
                          for player in start_moment.players]
        ball_circle = plt.Circle((0, 0), Constant.PLAYER_CIRCLE_SIZE,
                                 color=start_moment.ball.color)
        #xy_pos = [[0,0] for i in range(10)]
        
        #for circle in player_circles:
        #    xy_pos = np.column_stack((np.array(circle.center[0]), np.array(circle.center[1])))
            #print(circle.center)
        #print(xy_pos)
        #hull = ConvexHull(xy_pos)
        ############# 显示球员这个圈 ##################
        for circle in player_circles:
            ax.add_patch(circle)
            #xy_pos = np.column_stack((np.array(circle.center[0]), np.array(circle.center[1])))
            #print(circle)
        #polygon = Polygon(xy_pos, alpha = 1, color = 'green')    
        #xy_pos = [[1,4], [2,9], [5,8]]
        #xy_pos = np.column_stack((x,y))
        #xy_pos = np.array(xy_pos)
        #polygon = Polygon(xy_pos, color = 'b')
        ax.add_patch(ball_circle)
        ax.add_patch(home_xy_pos)
        ax.add_patch(visitor_xy_pos)
        ################################################
        anim = animation.FuncAnimation(
                         fig, self.update_radius,
                         fargs=(player_circles, ball_circle, annotations, clock_info,home_xy_pos,visitor_xy_pos, start),
                         frames= end, interval=Constant.INTERVAL,repeat = False)
        court = plt.imread("court.png")
        plt.imshow(court, zorder=0, extent=[Constant.X_MIN, Constant.X_MAX - Constant.DIFF,
                                            Constant.Y_MAX, Constant.Y_MIN]) 
        plt.show()

    ###########   当换人之后，重新生成整个模型 ############
    def final_show(self):       
        start_list = change.change_pos
        end_list = []
        start_list.insert(0,0)
        start_list.append(len(self.moments))
        for n in range(1,len(start_list)):
            end_list.append(start_list[n] - start_list[n - 1])
        for i in range(len(start_list)-1):
            self.show(start_list[i], end_list[i])
