import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class EndEffector:
    def __init__(self, start_pos,dimensions, blade_off,  danger_zone_offsets, approach_y_distance):

        self.approach_y_distance = approach_y_distance
        self.x_start, self.y_start, self.z_start = start_pos
        self.x_dim, self.y_dim, self.z_dim = dimensions
        self.danger_x, self.danger_y, self.danger_z = danger_zone_offsets
        self.angle = 0

        blade_x_off, blade_y_off, blade_z_off = blade_off
        blade_x = self.x_start + blade_x_off
        blade_y = self.y_start + blade_y_off
        blade_z = self.z_start + blade_z_off

        self.x_end = self.x_start + self.x_dim
        self.y_end = self.y_start + self.y_dim
        self.z_end = self.z_start + self.z_dim



        vertices = np.array([[self.x_start, self.y_start, self.z_start],
                             [self.x_end, self.y_start, self.z_start],
                             [self.x_end, self.y_end, self.z_start],
                             [self.x_start, self.y_end, self.z_start],
                             [self.x_start, self.y_start, self.z_end],
                             [self.x_end, self.y_start, self.z_end],
                             [self.x_end, self.y_end, self.z_end],
                             [self.x_start, self.y_end, self.z_end]])

        self.expanded_vertices = np.array([[self.x_start - self.danger_x, self.y_start - self.danger_y, self.z_start - self.danger_z],
                             [self.x_end + self.danger_x, self.y_start - self.danger_y, self.z_start - self.danger_z],
                             [self.x_end + self.danger_x, self.y_end + self.danger_y, self.z_start - self.danger_z],
                             [self.x_start - self.danger_x, self.y_end + self.danger_y, self.z_start - self.danger_z],
                             [self.x_start - self.danger_x, self.y_start - self.danger_y, self.z_end + self.danger_z],
                             [self.x_end + self.danger_x, self.y_start - self.danger_y, self.z_end + self.danger_z],
                             [self.x_end + self.danger_x, self.y_end + self.danger_y, self.z_end + self.danger_z],
                             [self.x_start - self.danger_x, self.y_end + self.danger_y, self.z_end + self.danger_z]], dtype = np.float)

        self.expansion_walls = self.get_expanded_walls().astype(np.float)
        self.expansion_pivot = np.array([
            self.x_start - self.danger_x  + (max(abs(self.x_start - self.danger_x), abs(self.x_end + self.danger_x))
                                             - min(abs(self.x_start - self.danger_x), abs(self.x_end + self.danger_x))) / 2,
            self.y_start - self.danger_y + (max(abs(self.y_start - self.danger_y), abs(self.y_end + self.danger_y))
                                            - min(abs(self.y_start - self.danger_y),
                                                  abs(self.y_end + self.danger_y))) / 2,
            self.z_start - self.danger_z ])

        self.vertices = vertices.astype(np.float)



        blade = np.array([blade_x, blade_y, blade_z])

        self.approach_line = np.array([blade, np.array([blade_x, blade_y + self.approach_y_distance, blade_z])])
        self.blade = blade

        self.danger_zone_offsets = danger_zone_offsets
        self.walls = self.get_walls()
        self.x_start, self.y_start, self.z_start = vertices[0]
        self.x_end, self.y_end, self.z_end = vertices[-1]
        self.pivot_point = np.array([self.x_start + self.x_dim/2, self.y_start + self.y_dim/2, self.z_start ])

        self.rotation_matrix = np.array([
                [np.cos(np.deg2rad(self.angle)), -np.sin(np.deg2rad(self.angle)), 0],
                [np.sin(np.deg2rad(self.angle)), np.cos(np.deg2rad(self.angle)), 0],
                [0, 0, 1]
            ])



    def check_colision(self, point):
        '''

        :param point - np.array([x,y,z]) in world frame:
        :return: True - if collision(danger/alarm) / False - no collision(safe)
        '''
        p = np.dot(np.linalg.inv(self.rotation_matrix), point - self.pivot_point)
        xmin = self.vertices[:,0].min()
        xmax = self.vertices[:,0].max()
        ymin = self.vertices[:,1].min()
        ymax = self.vertices[:,1].max()
        zmin = self.vertices[:,2].min()
        zmax = self.vertices[:,2].max()

        xc, yc, zc = False, False, False
        if p[0] >= xmin and p[0] <= xmax:
            xc = True
        if p[1] >= ymin and p[1] <= ymax:
            yc = True
        if p[2] >= zmin and p[2] <= zmax:
            zc = True
        # print('-'*20)
        # print('x')
        # print(f'{xmin}  - {p[0]} - {xmax} - {xc}')
        # print('y')
        # print(f'{ymin}  - {p[1]} - {ymax} - {yc}')
        # print('z')
        # print(f'{zmin}  - {p[2]} - {zmax} - {zc}')
        # print('-' * 20)
        if xc and yc and zc:
            return True
        else:
            return False

        # is_inside = (point >= self.vertices.min(axis=0)).all() and (point <= self.vertices.max(axis=0)).all()
        #
        # #is_inside = (point >= self.vertices.min(axis=0)).all() and (
        # #            point <= self.vertices.max(axis=0)).all()
        # if is_inside:
        #     return True
        # else:
        #     return False


    def goto(self, coordinate, angle = 0, pivot_point = 'pre'):
        #moves end effector pre-approach possition to desired position

        self.rotate(angle_degrees=angle)
        if pivot_point == 'pre':
            diff = coordinate - self.approach_line[-1]
        else:
            diff = coordinate - self.blade


        self.translate(diff)

    def rotate(self, angle_degrees, pp = 'st'):
        if pp == 'st':
            angle_radians = np.radians(angle_degrees)
            self.angle = angle_degrees
            self.vertices = self.vertices - self.pivot_point
            self.walls = self.walls - self.pivot_point
            self.approach_line = self.approach_line - self.pivot_point
            self.blade = self.blade - self.pivot_point

            self.rotation_matrix = np.array([
                [np.cos(angle_radians), -np.sin(angle_radians), 0],
                [np.sin(angle_radians), np.cos(angle_radians), 0],
                [0, 0, 1]
            ])

            self.vertices = np.dot(self.vertices, self.rotation_matrix ) + self.pivot_point
            self.walls = np.dot(self.walls, self.rotation_matrix ) + self.pivot_point
            self.approach_line = np.dot(self.approach_line, self.rotation_matrix ) + self.pivot_point
            self.blade = np.dot(self.blade, self.rotation_matrix ) + self.pivot_point


            self.expanded_vertices = self.expanded_vertices - self.expansion_pivot
            self.expansion_walls = self.expansion_walls - self.expansion_pivot

            self.expanded_vertices =  np.dot(self.expanded_vertices, self.rotation_matrix ) + self.expansion_pivot
            self.expansion_walls = np.dot(self.expansion_walls, self.rotation_matrix ) + self.expansion_pivot
        else:

            angle_radians = np.radians(angle_degrees)
            pp2  = self.approach_line[-1]
            self.pivot_point = self.approach_line[-1]
            self.angle = angle_degrees
            self.vertices = self.vertices - pp2
            self.walls = self.walls - pp2
            self.approach_line = self.approach_line - pp2
            self.blade = self.blade - pp2

            self.rotation_matrix = np.array([
                [np.cos(angle_radians), -np.sin(angle_radians), 0],
                [np.sin(angle_radians), np.cos(angle_radians), 0],
                [0, 0, 1]
            ])

            self.vertices = np.dot(self.vertices, self.rotation_matrix ) + pp2
            self.walls = np.dot(self.walls, self.rotation_matrix ) + pp2
            self.approach_line = np.dot(self.approach_line, self.rotation_matrix ) + pp2
            self.blade = np.dot(self.blade, self.rotation_matrix ) + pp2

            self.expanded_vertices = self.expanded_vertices - pp2
            self.expansion_walls = self.expansion_walls - pp2

            self.expanded_vertices = np.dot(self.expanded_vertices, self.rotation_matrix) + pp2
            self.expansion_walls = np.dot(self.expansion_walls, self.rotation_matrix) + pp2






    def translate(self, translation):
        self.blade += translation
        self.vertices += translation
        self.walls += translation
        self.pivot_point += translation
        self.approach_line += translation

        self.expansion_walls += translation
        self.expansion_pivot += translation
        self.expanded_vertices += translation



    def plot(self, ax):
        ax.plot(self.walls[:, 0],self.walls[:, 1], self.walls[:, 2], color='r')
        ax.scatter(self.vertices[:,0], self.vertices[:, 1], self.vertices[:, 2], color='r', marker='o')
        ax.scatter(self.blade[0], self.blade[1], self.blade[2], color='k', marker='x')
        ax.scatter(self.expanded_vertices[:, 0], self.expanded_vertices[:, 1], self.expanded_vertices[:,2], color = 'r', marker = 'o')
        ax.plot(self.expansion_walls[:, 0],self.expansion_walls[:, 1], self.expansion_walls[:, 2], 'r--' )

        ax.plot(self.approach_line[:,0], self.approach_line[:,1], self.approach_line[:,2], 'b--')


        return ax

    def get_walls(self ):
        walls = np.array([
            [self.x_start, self.y_start, self.z_start],
            [self.x_end, self.y_start, self.z_start],
            [self.x_end, self.y_end, self.z_start],
            [self.x_end, self.y_end, self.z_end],
            [self.x_end, self.y_start, self.z_end],
            [self.x_end, self.y_start, self.z_start],
            [self.x_start, self.y_start, self.z_start],
            [self.x_start, self.y_start, self.z_end],
            [self.x_end, self.y_start, self.z_end],
            [self.x_start, self.y_start, self.z_end],
            [self.x_start, self.y_end, self.z_end],
            [self.x_start, self.y_end, self.z_start],
            [self.x_start, self.y_start, self.z_start]
        ], dtype = np.float)
        return walls

    def get_expanded_walls(self):
        walls = np.array([
            [self.x_start - self.danger_x, self.y_start - self.danger_y, self.z_start - self.danger_z],
            [self.x_end + self.danger_x, self.y_start - self.danger_y, self.z_start - self.danger_z],
            [self.x_end + self.danger_x, self.y_end + self.danger_y, self.z_start - self.danger_z],
            [self.x_end + self.danger_x, self.y_end + self.danger_y, self.z_end + self.danger_z],
            [self.x_end + self.danger_x, self.y_start - self.danger_y, self.z_end + self.danger_z],
            [self.x_end + self.danger_x, self.y_start - self.danger_y, self.z_start - self.danger_z],
            [self.x_start - self.danger_x, self.y_start - self.danger_y, self.z_start - self.danger_z],
            [self.x_start - self.danger_x, self.y_start - self.danger_y, self.z_end + self.danger_z],
            [self.x_end + self.danger_x, self.y_start - self.danger_y, self.z_end + self.danger_z],
            [self.x_start - self.danger_x, self.y_start - self.danger_y, self.z_end + self.danger_z],
            [self.x_start - self.danger_x, self.y_end + self.danger_y, self.z_end + self.danger_z],
            [self.x_start - self.danger_x, self.y_end + self.danger_y, self.z_start - self.danger_z],
            [self.x_start - self.danger_x, self.y_start - self.danger_y, self.z_start - self.danger_z]
        ])

        return walls






if __name__ == '__main__':
    x_start = -30
    y_start = -30
    z_start = 1

    x_dim = 15
    y_dim = 15
    z_dim = 15

    blade_x_off = 7.5
    blade_y_off = 3
    blade_z_off = 1

    danger_zone_x = 3
    danger_zone_y = 3
    danger_zone_z = 0

    approach_distance = 20
    ef = EndEffector(start_pos = np.array([x_start, y_start, z_start]),
                     dimensions = np.array([x_dim, y_dim, z_dim]),
                     blade_off = np.array([blade_x_off, blade_z_off, blade_y_off]),
                     danger_zone_offsets= np.array([danger_zone_x, danger_zone_y, danger_zone_z]),
                     approach_y_distance = approach_distance)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    points = np.array([
        [-13, -13, 5], #danger_zone 1
        [-20, -20, 5], #inner_zone 1
        [0, 0, 0], #norm zone 1
        [0, 18, 5],  # danger_zone 2
        [0, 25, 5],  # inner_zone 2
        [-25, -25, -25],  # norm zone 2

    ])
    points = np.array([
        [-5, 38, 5], #danger zone 3
        [0, 30,5], #inner zone 3
        [-25,-25,25] #easy zone 3
    ])


    ef.plot(ax)
    ef.goto(np.array([10,10,10]), 45, 'pre')
    ef.plot(ax)
    ef.goto(np.array([20,20,20]), 45, 'pre')
    ef.plot(ax)
    plt.show()

