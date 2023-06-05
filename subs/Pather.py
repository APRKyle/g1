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
        self.rot_mat = np.array([[0.8958130477117826,0.17851346965270995,-0.24667315806556386],
        [-0.04057124310288974,-0.7508384723574618,-0.5685383533484816],
        [0.35864978902953326,-0.5625879043600538,0.6258790436005632]])

        self.trans_mat = np.array([116.6309639727365,-30.40538786108471,272.2236286919837])
        # bot camera
        # self.rot_mat = np.array([[0.753659597081984,0.025121986569399433,-0.03236871346441859],
        #                             [-0.015942799169041875,-1.0005314266389667,-0.0570075849074829],
        #                             [0.21691869172423983,-0.32610271027585847,1.3817092613169741]])
        # self.trans_mat = np.array([-38.16005604135472,-200.49084496835601,91.98149669066109])



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
            print(f' distance: {distance}')
            if spear.lenght > self.min_length:
                if distance < self.min_dist:
                    efficient_spear2d = efficient_spear2d
                    efficient_spear3d = botArm
                    stop_signal = True

        return stop_signal, efficient_spear2d, efficient_spear3d




