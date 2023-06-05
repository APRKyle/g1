import numpy as np
# sys.path.append('/usr/local/lib/python3.6/pyrealsense2')

# -96 -241 752
#
#
class Pather:
    def __init__(self, min_lenght, min_dist):

        self.min_length = min_lenght
        self.min_dist = min_dist
        # top camera
        # self.rot_mat = np.array([[0.8958130477117826,0.17851346965270995,-0.24667315806556386],
        # [-0.04057124310288974,-0.7508384723574618,-0.5685383533484816],
        # [0.35864978902953326,-0.5625879043600538,0.6258790436005632]])
        #
        # self.trans_mat = np.array([116.6309639727365,-30.40538786108471,272.2236286919837])

        self.rot_mat = np.array([[-1.2121212121212195, 2.424242424242439, -0.6060606060605876],
                      [-6.772727272727248, 6.5454545454545325, -1.6363636363635936],
                      [5.530303030303041, -6.060606060606071, 1.5151515151515067]])
        self.trans_mat = np.array([80.00000000000159, -249.49999999999866, 401.4999999999996])


    def _transformIntoRobot(self, coord):

        point = list(coord).copy()
        af_mat = np.array(self.rot_mat)
        trans_mat = np.array(self.trans_mat)
        trans_mat = trans_mat.reshape((-1, 1))
        tr = np.concatenate((af_mat, trans_mat), axis=1)
        tr = np.vstack((tr, [0, 0, 0, 0]))
        point.append(1)
        point = np.array(point).reshape((-1, 1))
        point = np.matmul(tr, point)
        point = np.delete(point, -1)


        return point



    def processSpears(self, spears):
        efficient_spear2d = False
        stop_signal = None
        efficient_spear3d = None

        for idx, spear in enumerate(spears):
            if np.all(spear.bot_3d == 0):
                print('unreachable depth')
                continue
            botArm = self._transformIntoRobot(spear.bot_3d)
            distance = np.linalg.norm(botArm)
            print(f'distance: {distance}')
            if spear.lenght > self.min_length:
                if distance < self.min_dist:
                    efficient_spear2d = efficient_spear2d
                    efficient_spear3d = botArm
                    stop_signal = True

        return stop_signal, efficient_spear2d, efficient_spear3d




