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
        # self.rot_mat = np.array([[0.9487146026360417,0.2544695289051286,-0.181391100091348],
        #                         [-0.0013049719431084037,-0.7568837269998696,-0.7425290356257361],
        #                         [0.3438601070077006,-0.5611379355343884,0.6564008873809208]])
        #
        # self.trans_mat = np.array([124.59611118360957,-1.5166383922740176,225.63421636434902])

        self.rot_mat = np.array([[0.8418942620897019,0.2842081706740937,-0.1801190082265248],
                                [0.052618391380606346,-0.6549469129969911,-0.6267154532813342],
                                [0.38336256577298783,-0.6169032995996714,0.6029597127888898]])

        self.trans_mat = np.array([122.09794556836873,-59.30303870732044,254.0298782948655])



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
            cd = np.linalg.norm(spear.bot_3d)
            print(f'camera distance: {cd}')
            botArm = self._transformIntoRobot(spear.bot_3d)
            distance = np.linalg.norm(botArm)
            print(f'distance: {distance}')

            if spear.lenght > self.min_length:
                if distance < self.min_dist:
                    if cd < 820:
                        if botArm[0] < 10:
                            efficient_spear2d = efficient_spear2d
                            efficient_spear3d = botArm
                            stop_signal = True

        return stop_signal, efficient_spear2d, efficient_spear3d




