import numpy as np
from .Spear import Spear



class AsparagusProcessor:
    def __init__(self, camera, topk = 0.06, botk = 0.06):
        self.topk = topk
        self.botk = botk
        self.camera = camera


    def process(self, boxes, masks):
        spears = []

        for idx, (box, mask) in enumerate(zip(boxes, masks)):

            mask[np.logical_and(mask == 1, self.camera.depthNP == 0)] = 0
            mask = mask.astype(np.int)

            asparagusMask = np.where(mask == 1)

            print(f'mask shape: {mask.shape}')
            asparagus = np.array([asparagusMask[0], asparagusMask[1]])
            print(f'0 min: {asparagus[0].min()} max: {asparagus[0].max()}')
            print(f'1 min: {asparagus[1].min()} max: {asparagus[1].max()}')
            length2d = box[3] - box[1]
            bot_part = asparagus[:, asparagus[0] > box[3] - length2d * self.botk]
            #length2d = asparagus[0].max() - asparagus[0].min()
            #bot_part = asparagus[:, asparagus[0] > asparagus[0].max() - length2d*self.botk]
            #same with top part buth change max to min

            bot_point = np.mean(bot_part, axis=1).astype(np.int)[::-1]

            top_part = asparagus[:,asparagus[0] < box[1] + length2d * self.topk]
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
