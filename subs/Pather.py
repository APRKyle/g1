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
        self.rot_mat = np.array([[0.8257882034648663,0.3261955636173577,-0.3544801930733394],
                                [0.03781531981615042,-0.7520022135796963,-0.6342520713879454],
                                [0.509738213456718,-0.5432493505295676,0.6374802084454195]])

        self.trans_mat = np.array([109.72099672574637,-34.08723656095816,230.02733156042038])


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

        for spear in spears:

            top = np.array(self.camera._calculatePix3D(spear[0], depthFrame))
            bot = np.array(self.camera._calculatePix3D(spear[1], depthFrame))
            botArm = self._transformIntoRobot(bot)
            length = np.linalg.norm(top - bot)
            distance = np.linalg.norm(botArm)
            print(f'length {length}  D {distance} | P : {botArm}')
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

