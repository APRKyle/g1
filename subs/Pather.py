import numpy as np
# sys.path.append('/usr/local/lib/python3.6/pyrealsense2')

# -96 -241 752
#
#
class Pather:
    def __init__(self, camera, min_lenght, min_dist):
        self.camera = camera
        self.min_length = min_lenght
        self.min_dist = min_dist
        # top camera
        # self.rot_mat = np.array([[0.7702721628308652,0.3426544045562763,-0.383268754960085],
        #                         [0.03585266794267323,-0.7549600858970162,-0.6432939638672319],
        #                         [0.5090331917277439,-0.510527052892021,0.658232575510013]])
        #
        # self.trans_mat = np.array([119.34876989869718,-30.90303907380613,222.6787264833573])
        # bot camera
        self.rot_mat = np.array([[0.11914308626417655,1.7275747508305608,-0.7343338297628568],
                                    [-0.0025203345171267966,-1.0365448504983366,-0.04215832283193922],
                                    [0.034291824187574226,0.16389811738649016,1.1796693015618431]])
        self.trans_mat = np.array([227.48252949936926,-206.1102073547941,168.43888188795952])

    def process(self, points, depthFrame):

        efficientSpear = self._choseClosesCoord(points, depthFrame)

        return efficientSpear

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



    def processSpears(self, spears, depthFrame):


        if len(spears) == 0:
            return False, None, None
        top = None
        bot = None
        for idx, spear in enumerate(spears):

            top = np.array(self.camera._calculatePix3D(spear[0], depthFrame))
            bot = np.array(self.camera._calculatePix3D(spear[1], depthFrame))
            if np.all(bot == 0):
                return False, None, None
            botArm = self._transformIntoRobot(bot)
            length = np.linalg.norm(top - bot)
            distance = np.linalg.norm(botArm)
            print(f'{idx}:   length {length}  D {distance} | P: {botArm}  F: {bot}')
            if length > self.min_length:
                if distance < self.min_dist:
                    return True, spear, botArm
        return False, None, None

    def _choseClosesCoord(self, coords, depthFrame):

        mindist = np.inf
        efficientSpear = None
        if coords is not None:
            for point in coords:
                coord = self.camera._calculatePix3D(point, depthFrame)
                coord2 = self._transformIntoRobot(coord)

                if np.any(coord2):
                    dist = np.linalg.norm(coord2)
                    if dist < mindist:
                        mindist = dist
                        efficientSpear = coord2

        return efficientSpear

