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




        # self.rot_mat = np.array([[0.8518047817790189,0.19397420588449865,-0.21770264199625988],
        #                         [0.06266150118834103,-0.7788340814061976,-0.533256286307771],
        #                         [0.35880620625309484,-0.5166694183461504,0.6689460811604657]])
        # self.trans_mat = np.array([113.64838143653039,-47.81207308972683,134.59630942187866])

        self.rot_mat = np.array([[0.841288303420094, 0.19415228395321518, -0.11879847111532792],
                                 [0.03655779038669746, -0.6648697042855437, -0.6661896872979363],
                                 [0.32695405311305564, -0.6715270099132626, 0.5882532990010203]])
        self.trans_mat = np.array([117.88510026131836, -124.97572761672279, 129.7476919427471])



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
            botArm = self._transformIntoRobot(spear.bot_3d)
            topArm = self._transformIntoRobot(spear.top_3d)
            distance = np.linalg.norm(botArm)
            lin_dist = abs(topArm[1] - botArm[1])
            print(f'lin dist: {lin_dist}')
            print(f'distance: {distance}')
            print(f'botArm  : {botArm}')
            print(f'topArm  : {topArm}')
            print(f'lenght  : {spear.lenght}')

            if spear.lenght > self.min_length:
                if distance < self.min_dist:
                    if lin_dist > 130:
                        efficient_spear2d = efficient_spear2d
                        efficient_spear3d = botArm
                        stop_signal = True
                        angle = 0

                else:
                    if lin_dist > 130:
                        efficient_spear2d = efficient_spear2d
                        efficient_spear3d = botArm
                        stop_signal = True
                        angle = 45



        return stop_signal, efficient_spear2d, efficient_spear3d, angle




