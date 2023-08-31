import numpy as np
# sys.path.append('/usr/local/lib/python3.6/pyrealsense2')

# -96 -241 752
#
#
class Pather:
    def __init__(self, min_lenght, min_dist, max_distance):

        self.min_length = min_lenght
        self.min_dist = min_dist
        self.max_distance = max_distance
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
        angle = None

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







    def _calculateBotArmDistance(self, spear):
        #transformed bot point into robot frame and calculate distance to it

        botArm = None
        distanceToBot = None
        cameraAcessabilityFlag = False
        if np.all(spear.bot_3d == 0):
            return botArm, distanceToBot, cameraAcessabilityFlag

        botArm = self._transformIntoRobot(spear.bot_3d)
        distance2Bot = np.linalg.norm(botArm)
        cameraAcessabilityFlag  = True
        return botArm, distance2Bot, cameraAcessabilityFlag


    def _maxHeightDistanceFilter(self, spear):

        #filters spear accordint to spear height and robot max reachable distance

        robotAcessabilityFlag = 0  #states 0 - unassseible, 1 - accesible, 2 - acessible with angle correction according to min dist

        botArm, distance2Bot, cameraAcessabilityFlag  = self._calculateBotArmDistance(spear)
        print(f'cam Acess: {cameraAcessabilityFlag}')
        if cameraAcessabilityFlag :

            if spear.lenght < self.min_length:
                robotAcessabilityFlag = 0
                return botArm, distance2Bot,  robotAcessabilityFlag

            if distance2Bot > self.max_distance:
                robotAcessabilityFlag = 0
                return botArm, distance2Bot, robotAcessabilityFlag

            if distance2Bot < self.min_dist:
                robotAcessabilityFlag = 2
                return botArm, distance2Bot, robotAcessabilityFlag

            robotAcessabilityFlag = 1
            return botArm, distance2Bot, robotAcessabilityFlag

        else:
            robotAcessabilityFlag = 0
            return botArm, distance2Bot, robotAcessabilityFlag


    def processMain(self, spears):
        #botArm, distance2Bot, angle, stopSignal

        botArm = None
        distance2Bot = None
        angle = None
        stopSignal = None

        data = []
        for idx, spear in enumerate(spears):
            botArm, distance2Bot, robotAcessabilityFlag = self._maxHeightDistanceFilter(spear)
            if robotAcessabilityFlag != 0:
                data.append([spear, botArm, distance2Bot, robotAcessabilityFlag])
        print(len(data))
        #no any spear
        if len(data) == 0:
            return botArm, distance2Bot, angle, stopSignal
        #only one spear
        if len(data) == 1:

            spear = data[0][0]
            robotAcessabilityFlag= data[0][-1]
            if robotAcessabilityFlag == 0:
                return botArm, distance2Bot, angle, stopSignal



            if robotAcessabilityFlag == 1:
                spearPitch = round(spear.pitch)
                if abs(spearPitch) < 50 and abs(spearPitch) > 40:
                    angle = 0
                else:
                    if spearPitch > 0:
                        angle = (90 - spearPitch) * -1
                    else:
                        angle = 90 - spearPitch * -1
                return botArm, distance2Bot, angle, stopSignal

            if robotAcessabilityFlag == 2:
                spearPitch = round(spears[0].pitch)
                if abs(spearPitch) < 50 and abs(spearPitch) > 40:
                    angle = 90
                else:
                    if spearPitch > 0:
                        angle = -90
                    else:
                        angle = 90
                return botArm, distance2Bot, angle, stopSignal




        else:
            # data : [
            #         [spear, botArm, distance2Bot, robotAcessabilityFlag]
            #
            # ]

            minv = np.inf
            lowestidx = None

            for idx, v in enumerate(data):
                if data[2] < minv:
                    minv = data[2]
                    lowestidx = idx

            ans, distance = calculateHorizontalDistance2All(data, lowestidx)
            if data[2] < self.min_dist:

                if distance < 0:
                    angle = 90
                else:
                    angle = -90

            else:
                if distance < 0:
                    angle = 45
                else:
                    angle = -45


            return data[lowestidx][2], data[lowestidx][2], angle, True



def calculateHorizontalDistance2All(data, bidx):
    ans = {}
    closesOnX = np.inf
    for idx, value in enumerate(data):
        if idx == bidx:
            continue
        distance = data[bidx][1][0] - value[1][0]
        ans[idx] = distance
        if abs(distance) < abs(closesOnX):
            closesOnX = distance
    return ans, distance








