import numpy as np
# sys.path.append('/usr/local/lib/python3.6/pyrealsense2')

# -96 -241 752
#
#
class Pather:
    def __init__(self, min_lenght, min_distance_w_no_angle_correction, max_reachable_distance):

        self.min_length = min_lenght
        self.min_distance_w_no_angle_correction = min_distance_w_no_angle_correction
        self.max_reachable_distance = max_reachable_distance
        # top camera


        # self.rot_mat = np.array([[0.9022556390977434,0.19480519480519412,-0.24606971975393072],
        #                         [-0.002622836160167983,-0.7814859559045599,-0.49082802142777604],
        #                         [0.34621437314215736,-0.48021745696164103,0.6983897375574247]])
        #
        # self.trans_mat = np.array([122.99726589200256,-42.55390325708568,254.56977538984853])

        self.rot_mat = np.array(    [[0.9006824488163374, 0.25594508983254777, -0.18684312962242106],
                                 [0.005999550033748842, -0.622774720467394, -0.7006617360840779],
                                 [0.3989700772442051, -0.7002331967959551, 0.5488516932658601]])
        self.trans_mat = np.array([131.989565068334, -124.83270897539833, 144.33913885030037])



    def _calc_rob_pickofs(self, spears):
        for spear in spears:
            spear.arm_bot_3d = self._transformIntoRobot(spear.bot_3d)
            spear.arm_bot_3d_2 = np.array([spear.arm_bot_3d[0], spear.arm_bot_3d[2], spear.arm_bot_3d[1]])
        return True

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

            if spear.length < self.min_length:
                continue



            botArm = self._transformIntoRobot(spear.bot_3d)
            distance = np.linalg.norm(botArm)


            if distance < self.min_distance_w_no_angle_correction:
                if botArm[0] < 10:
                    efficient_spear2d = efficient_spear2d
                    efficient_spear3d = botArm
                    stop_signal = True

        return stop_signal, efficient_spear2d, efficient_spear3d


    #function
    #return dict{spear : approach flag}

    def _filter_height_distance(self, spears):

        #flag_description
        # [length, min, max]
        # length:
        #   0 - low on length
        #   1 - good on length
        # min:
        #   0 - far from robot
        #   1 - close to robot
        # max:
        #   0 - closer then max dist
        #   1 - further then reach

        data = {}
        for spear in spears:
            data[spear] = [0,0,0]
            #-------------spear length check-------------
            if spear.lenght >= self.min_length:
                data[spear][0] = 1
            else:
                data[spear][0] = 0
            #--------------------------------------------

            #       bot arm transformation and distance check
            botArm, distance2Bot, cameraAcessabilityFlag = self._calculateBotArmDistance(spear)
            if distance2Bot is None:
                spear.arm_bot_3d = [0,0,0]
                return data

            # -------------far away spear limits-------------
            if distance2Bot > self.max_reachable_distance:
                data[spear][2] = 1
            else:
                data[spear][2] = 0

            # -------------far away spear limits-------------
            #  -----close spears should be angled flag-------
            if botArm[-1] < self.min_distance_w_no_angle_correction:
                spear.arm_bot_3d = botArm
                data[spear][1] = 1
            else:
            #  -----perfect match spear-------
                spear.arm_bot_3d = botArm
                data[spear][1] = 0

        return data

    def height_filter(self, spears):
        data = []
        for spear in spears:
            if spear.lenght >= self.min_length:
                data.append(spear)
        return data

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

        if cameraAcessabilityFlag :

            if spear.lenght < self.min_length:
                robotAcessabilityFlag = 0
                return botArm, distance2Bot,  robotAcessabilityFlag

            if distance2Bot > self.max_reachable_distance:

                robotAcessabilityFlag = 0
                return botArm, distance2Bot, robotAcessabilityFlag

            if distance2Bot < self.min_distance_w_no_angle_correction:

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

        #no any spear
        if len(data) == 0:
            print('no spears')
            return botArm, distance2Bot, angle, stopSignal
        #only one spear
        if len(data) == 1:
            print('one spear')
            spear = data[0][0]
            robotAcessabilityFlag= data[0][-1]
            print(f'acessability flag: {robotAcessabilityFlag}')
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
                        angle = (90 - spearPitch * -1) * -1
                return data[0][1], data[0][2], angle, True

            if robotAcessabilityFlag == 2:
                spearPitch = round(spears[0].pitch)
                if abs(spearPitch) < 50 and abs(spearPitch) > 40:
                    angle = 90
                else:
                    if spearPitch > 0:
                        angle = -90
                    else:
                        angle = 90
                return data[0][1], data[0][2], angle, True




        else:
            print('more then 1 spears')
            # data : [
            #         [spear, botArm, distance2Bot, robotAcessabilityFlag]
            #
            # ]

            minv = np.inf
            lowestidx = None

            for idx, v in enumerate(data):
                if v[2] < minv:
                    minv = v[2]
                    lowestidx = idx

            ans, distance = calculateHorizontalDistance2All(data, lowestidx)
            if data[lowestidx][2] < self.min_distance_w_no_angle_correction:
                print('spear is close to robot')
                if distance < 0:
                    angle = 90
                else:
                    angle = -90

            else:
                if distance < 0:
                    print('distance between spears is less then zero (closest spear is on the right)')
                    angle = 60
                else:
                    print('distance between spears is more then zero (closest spear is on the right)')
                    angle = -60


            return data[lowestidx][1], data[lowestidx][2], angle, True



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


#general logic:
#   receive all spears from asparagus processor
#       depth unrechable
#       distance from the camera(z distance only) ignored








