import numpy as np
# sys.path.append('/usr/local/lib/python3.6/pyrealsense2')



class Pather:
    def __init__(self, camera, min_lenght, min_dist):
        self.camera = camera
        self.min_length = min_lenght
        self.min_dist = min_dist
        self.rot_mat = np.array([[0.8491508491508474, 0.2997002997002997, -0.35964035964035973],
                      [0.2007992007992008, -0.9585414585414578, -0.7497502497502503],
                      [0.7527472527472496, -0.7637362637362624, 0.516483516483516]])

        self.trans_mat = np.array([116.40359640359611, -6.997502497502614, 258.1648351648353])



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
        point[1] += 0
        point[2] -= 0

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

