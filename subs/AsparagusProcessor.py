import numpy as np
from .Spear import Spear



class AsparagusProcessor:
    def __init__(self, camera, topk = 0.06, botk = 0.06, ignore_distance = 400 ):
        self.topk = topk
        self.botk = botk
        self.camera = camera
        self.ignore_distance = ignore_distance   # ground distance (distance from the camera to ignore)


    def process(self, boxes, masks):
        spears = []
        data = {}
        for idx, (box, mask) in enumerate(zip(boxes, masks)):

            mask[np.logical_and(mask == 1, self.camera.depthNP == 0)] = 0  # stereo unreachable pixels distance check
            mask[np.logical_and(mask == 1, self.camera.depthNP > self.ignore_distance)] = 0

            if np.all(np.all(mask == 0)):
                continue
            mask = mask.astype(np.int)

            asparagusMask = np.where(mask == 1)


            asparagus = np.array([asparagusMask[0], asparagusMask[1]])
            #asparagus: 0 -  y coordinate, 1 - x coordinate

            length2d = asparagus[0].max() - asparagus[0].min()
            bot_part = asparagus[:, asparagus[0] > asparagus[0].max() - length2d * self.botk]
            top_part = asparagus[:, asparagus[0] < asparagus[0].min() + length2d * self.topk]



            skeleton, bot_point, top_point = self.split_into_n_pices(20, asparagus, self.topk, self.botk)
            skeleton3d = self.calculate_batch_3d(skeleton)
            top_3d = self.camera._calculatePix3D(top_point)
            bot_3d = self.camera._calculatePix3D(bot_point)
            length = np.linalg.norm(bot_3d - top_3d)

            pitch_deg, yaw_deg, roll_deg = self.get_angles(np.array(skeleton3d))

            spear = Spear(box=box, mask=mask, bot_point=bot_point, top_point=top_point, top_3d=top_3d,
                          bot_3d=bot_3d, lenght=length, id=idx, skeleton=skeleton, skeleton_3d=skeleton3d,
                          roll=roll_deg, yaw=yaw_deg, pitch=pitch_deg)

            spears.append(spear)

            data[idx] = spear.to_dict()


        return spears, data

    def _remove_outliers(self, data):

        Q1 = np.percentile(data, 25, axis=0)
        Q3 = np.percentile(data, 75, axis=0)
        IQR = Q3 - Q1
        threshold_multiplier = 1.5
        outlier_mask = (data < Q1 - threshold_multiplier * IQR) | (data > Q3 + threshold_multiplier * IQR)
        cleaned_data = data[~np.any(outlier_mask, axis=1)]

        return cleaned_data

    def calculate_batch_3d(self, points):
        res = []
        for p in points:
            p3d = self.camera._calculatePix3D(p)
            if np.array_equal(p3d, np.array([0, 0, 0])):
                pass
            else:
                res.append(p3d.tolist())
        return res

    def split_into_n_pices(self, n, indexes, topk, botk):

        dist = indexes[0].max() - indexes[0].min()
        step = dist // n
        c = indexes[0].min()
        res = []
        for i in range(n):
            part = indexes[:, np.logical_and(indexes[0] >= c, indexes[0] <= c + step)]

            mean = np.mean(part, axis=1).astype(np.int)[::-1]
            res.append(mean)

            c = c + step
        res = self._remove_outliers(np.array(res))
        res = res.tolist()
        bot_part = indexes[:, indexes[0] > indexes[0].max() - dist * botk]
        top_part = indexes[:, indexes[0] < indexes[0].min() + dist * topk]
        bot_point = np.mean(bot_part, axis=1).astype(np.int)[::-1]
        top_point = np.mean(top_part, axis=1).astype(np.int)[::-1]
        return res, bot_point, top_point


    def get_angles(self, data):
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