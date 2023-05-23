import numpy as np
# sys.path.append('/usr/local/lib/python3.6/pyrealsense2')



class Pather:
    def __init__(self, camera, min_lenght, min_dist):
        self.camera = camera
        self.min_length = min_lenght
        self.min_dist = min_dist
        self.rot_mat = np.array([[1.0047055627901034, -0.012462950683464952, -0.009427103722108292],
                                 [0.11967628284506707, -0.860263159997121, -0.13789136461320725],
                                 [0.09570906999224837, -0.2874467728147885, 1.0646235949221439]])

        self.trans_mat = np.array([-63.383810946624905, -312.80048893114093, 176.3785141925851])

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
        point[1] += 30
        point[2] -= 25

        return point



    def processSpears(self, spears, depthFrame):


        if len(spears) == 0:
            return False, None, None

        for spear in spears:

            top = np.array(self.camera._calculatePix3D(spear[0], depthFrame))
            bot = np.array(self.camera._calculatePix3D(spear[1], depthFrame))
            botArm = self._transformIntoRobot(bot)
            length = np.linalg.norm(top - bot)
            distance = np.linalg.norm(botArm)
            print(f'length {length}  D {distance}')
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

