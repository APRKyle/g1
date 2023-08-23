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


        # self.rot_mat = np.array([[0.9022556390977434,0.19480519480519412,-0.24606971975393072],
        #                         [-0.002622836160167983,-0.7814859559045599,-0.49082802142777604],
        #                         [0.34621437314215736,-0.48021745696164103,0.6983897375574247]])
        #
        # self.trans_mat = np.array([122.99726589200256,-42.55390325708568,254.56977538984853])

        self.rot_mat = np.array([[0.8518047817790189,0.19397420588449865,-0.21770264199625988],
                                [0.06266150118834103,-0.7788340814061976,-0.533256286307771],
                                [0.35880620625309484,-0.5166694183461504,0.6689460811604657]])
        self.trans_mat = np.array([113.64838143653039,-47.81207308972683,134.59630942187866])



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

            if spear.length < self.min_length:
                continue



            botArm = self._transformIntoRobot(spear.bot_3d)
            distance = np.linalg.norm(botArm)


            if distance < self.min_dist:
                if botArm[0] < 10:
                    efficient_spear2d = efficient_spear2d
                    efficient_spear3d = botArm
                    stop_signal = True

        return stop_signal, efficient_spear2d, efficient_spear3d




