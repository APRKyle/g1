import numpy as np
from .Spear import Spear



class AsparagusProcessor:
    def __init__(self, camera, topk = 0.06, botk = 0.06):
        self.topk = topk
        self.botk = botk
        self.camera = camera


    def process(self, boxes, masks):
        spears = []
        unreachable = np.where(self.camera.depthNP == 0)
        for idx, (box, mask) in enumerate(zip(boxes, masks)):


            asparagusMask = np.where(mask == 1)

            m1 = unreachable[0] == asparagusMask[0]
            m2 = unreachable[1] == asparagusMask[1]
            m3 = m1*m2
            print(f'unreachable: {unreachable}')
            print(f' unreachable and saparagus: {np.where(m3 == True)}')
            asparagus = np.array([asparagusMask[0][m3], asparagusMask[1][m3]])

            length2d = box[3] - box[1]
            print(f'asparagus after: {asparagus}')
            print(f'length 2d : {length2d}')
            print(f'boxes: {boxes}')
            bot_part = asparagus[:, asparagus[0] > box[3] - length2d * self.botk]

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
