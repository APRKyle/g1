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


        self.vertices = vertices.astype(np.float)

        self.angle = 0
        blade = np.array([blade_x, blade_y, blade_z], dtype = float)

        self.approach_line = np.array([blade, np.array([blade_x, blade_y + self.approach_y_distance, blade_z])])
        self.blade = blade

        self.danger_zone_offsets = danger_zone_offsets
        self.walls = self.get_walls()
        self.x_start, self.y_start, self.z_start = vertices[0]
        self.x_end, self.y_end, self.z_end = vertices[-1]
        self.pivot_point = np.array([self.x_start + self.x_dim/2, self.y_start + self.y_dim/2, self.z_start ], dtype = float)

        self.rotation_matrix = np.array([
                [np.cos(np.deg2rad(self.angle)), -np.sin(np.deg2rad(self.angle)), 0],
                [np.sin(np.deg2rad(self.angle)), np.cos(np.deg2rad(self.angle)), 0],
                [0, 0, 1]
            ])

    import numpy as np

    def inside_test(self, points):
        print(points)
        """
        cube3d  =  numpy array of the shape (8,3) with coordinates in the clockwise order. First, the bottom plane is considered, then the top one.
        points = array of points with shape (N, 3).

        Returns the indices of the points array which are outside the cube3d
        """
        b1, b2, b3, b4, t1, t2, t3, t4 = self.vertices

        dir1 = (t1 - b1)
        size1 = np.linalg.norm(dir1)
        dir1 = dir1 / size1

        dir2 = (b2 - b1)
        size2 = np.linalg.norm(dir2)
        dir2 = dir2 / size2

        dir3 = (b4 - b1)
        size3 = np.linalg.norm(dir3)
        dir3 = dir3 / size3

        cube3d_center = (b1 + t3) / 2.0

        dir_vec = points - cube3d_center

        dot_product1 = np.abs(np.dot(dir_vec, dir1)) * 2
        dot_product2 = np.abs(np.dot(dir_vec, dir2)) * 2
        dot_product3 = np.abs(np.dot(dir_vec, dir3)) * 2

        outside_indices = np.where(
            (dot_product1 > size1) |
            (dot_product2 > size2) |
            (dot_product3 > size3)
        )[0]

        return outside_indices




    def check_colision(self, point):
        r = self.inside_test(point)
        print(r)
        if len(r) == 0:
            return True, point
        else:
            return False, point




    def goto(self, coordinate, angle = 0, pivot_point = 'pre'):
        #moves end effector pre-approach possition to desired position
        if angle != self.angle:

            target_angle = (self.angle - angle) * -1
            self.angle = angle
            self.rotate(angle_degrees=target_angle)
            if pivot_point == 'pre':
                diff = coordinate - self.approach_line[-1]
            else:
                diff = coordinate - self.blade

            self.translate(diff)
        else:
            if pivot_point == 'pre':
                diff = coordinate - self.approach_line[-1]
            else:
                diff = coordinate - self.blade
            self.translate(diff)

    def rotate(self, angle_degrees, pp = 'st'):

        if pp == 'st':
            angle_radians = np.radians(angle_degrees)

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


        else:

            angle_radians = np.radians(angle_degrees)

            self.pivot_point = self.approach_line[-1]
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


    def translate(self, translation):
        self.blade += translation
        self.vertices += translation
        self.walls += translation
        self.pivot_point += translation
        self.approach_line += translation


    def plot(self, ax):
        ax.scatter(self.pivot_point[0], self.pivot_point[1], self.pivot_point[2], color = 'y', marker = '*')
        ax.plot(self.walls[:, 0],self.walls[:, 1], self.walls[:, 2], color='r')
        ax.scatter(self.vertices[:,0], self.vertices[:, 1], self.vertices[:, 2], color='r', marker='o')
        ax.scatter(self.blade[0], self.blade[1], self.blade[2], color='k', marker='x')
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
    ax.set_xlim(-50,20)
    ax.set_ylim(-50, 20)
    ax.set_zlim(-5, 30)


    p = np.array([5, 5, 5])
    ax.scatter(p[0], p[1], p[2], marker='o', color='k')


    ef.plot(ax)


    ef.goto(np.array([-10,-10,5]), angle = 45, pivot_point = 'pre')
    p = np.dot(np.linalg.inv(ef.rotation_matrix), p - ef.pivot_point)
    p = p + ef.pivot_point
    ax.scatter(p[0], p[1], p[2], marker='o', color='r')
    ef.plot(ax)



    plt.show()

