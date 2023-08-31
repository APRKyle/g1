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
        angle = None
        for idx, spear in enumerate(spears):
            if np.all(spear.bot_3d == 0):
                continue
            botArm = self._transformIntoRobot(spear.bot_3d)
            topArm = self._transformIntoRobot(spear.top_3d)
            distance = np.linalg.norm(botArm)
            lin_dist = abs(topArm[1] - botArm[1])


            if spear.lenght > self.min_length:
                if distance < self.min_dist:
                    if lin_dist > 130:
                        efficient_spear2d = efficient_spear2d
                        efficient_spear3d = botArm
                        stop_signal = True
                        angle = 45

                else:
                    if lin_dist > 130:
                        efficient_spear2d = efficient_spear2d
                        efficient_spear3d = botArm
                        stop_signal = True
                        angle = 0



        return stop_signal, efficient_spear2d, efficient_spear3d, angle





    def _getAngles(self, data):
        centroid = np.mean(data, axis=0)
        translated_points = data - centroid
        covariance_matrix = np.cov(translated_points, rowvar=False)
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
        dominant_eigenvector = eigenvectors[:, np.argmax(eigenvalues)]
        dominant_eigenvector /= np.linalg.norm(dominant_eigenvector)
        pitch = np.arcsin(dominant_eigenvector[2])
        yaw = np.arctan2(dominant_eigenvector[1], dominant_eigenvector[0])
        roll = 0

        pitch_deg = np.degrees(pitch)
        yaw_deg = np.degrees(yaw)
        roll_deg = np.degrees(roll)
        return pitch_deg, yaw_deg, roll_deg


