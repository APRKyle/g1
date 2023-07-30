import numpy as np
from .Spear import Spear



class AsparagusProcessor:
    def __init__(self, camera, topk = 0.06, botk = 0.06, ignore_distance = 200 ):
        self.topk = topk
        self.botk = botk
        self.camera = camera
        self.ignore_distance = ignore_distance


    def process(self, boxes, masks):
        spears = []

        for idx, (box, mask) in enumerate(zip(boxes, masks)):

            mask[np.logical_and(mask == 1, self.camera.depthNP == 0)] = 0  # stereo unreachable pixels distance check
            print(f'min: {self.camera.depthNP.min()}  max: {self.camera.depthNP.max()}')
            mask = mask.astype(np.int)

            asparagusMask = np.where(mask == 1)


            asparagus = np.array([asparagusMask[0], asparagusMask[1]])
            #asparagus: 0 -  y coordinate, 1 - x coordinate

            length2d = asparagus[0].max() - asparagus[0].min()
            bot_part = asparagus[:, asparagus[0] > asparagus[0].max() - length2d * self.botk]
            top_part = asparagus[:, asparagus[0] < asparagus[0].min() + length2d * self.topk]

            bot_point = np.mean(bot_part, axis=1).astype(np.int)[::-1]
            top_point = np.mean(top_part, axis=1).astype(np.int)[::-1]


            bot_point3d = self.camera._calculatePix3D(bot_point)
            top_point3d = self.camera._calculatePix3D(top_point)
            length = np.linalg.norm(bot_point3d - top_point3d)


            spears.append(Spear(box = box, mask = mask,
                                 top_point = top_point, bot_point = bot_point,
                                 top_3d=top_point3d, bot_3d = bot_point3d,
                                 lenght = length, id = idx,
                                 ))


        return spears
