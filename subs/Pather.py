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
        # self.rot_mat = np.array([[0.7702721628308652,0.3426544045562763,-0.383268754960085],
        #                         [0.03585266794267323,-0.7549600858970162,-0.6432939638672319],
        #                         [0.5090331917277439,-0.510527052892021,0.658232575510013]])
        #
        # self.trans_mat = np.array([119.34876989869718,-30.90303907380613,222.6787264833573])
        # bot camera
        self.rot_mat = np.array([[0.753659597081984,0.025121986569399433,-0.03236871346441859],
                                    [-0.015942799169041875,-1.0005314266389667,-0.0570075849074829],
                                    [0.21691869172423983,-0.32610271027585847,1.3817092613169741]])
        self.trans_mat = np.array([-38.16005604135472,-200.49084496835601,91.98149669066109])



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

            if spear.lenght > self.min_length:
                if distance < self.min_dist:
                    efficient_spear2d = botArm
                    efficient_spear3d = efficient_spear3d
                    stop_signal = True

        return stop_signal, efficient_spear2d, efficient_spear3d




