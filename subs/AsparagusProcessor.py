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


            asparagus = np.where(mask == 1)
            asparagus = np.array([asparagus[0], asparagus[1]])

            indices = np.where((unreachable[0] != asparagus[0]) | (unreachable[1] != asparagus[1]))
            asparagus = np.array([unreachable[0][indices], asparagus[1][indices]])

            length = box[3] - box[1]
            # bot_part = asparagus[:, asparagus[0] > box[3] - length * self.botk]
            # bot_point = np.mean(bot_part, axis=1).astype(np.int)[::-1]
            # top_part = asparagus[:, asparagus[0] < box[1] + length * self.topk]
            # top_point = np.mean(top_part, axis=1).astype(np.int)[::-1]

            bot_part = asparagus[:, asparagus[0] > box[3] - length * self.botk]

            bot_point = np.mean(bot_part, axis=1).astype(np.int)[::-1]

            top_part = asparagus[:, asparagus[0] < box[1] + length * self.topk]
            top_point = np.mean(top_part, axis=1).astype(np.int)[::-1]


            bot_point3d = self.camera._calculatePix3D(bot_point)
            top_point3d = self.camera._calculatePix3D(top_point)
            length = np.linalg.norm(bot_point3d - top_point3d)

            # pcdata = self.camera.depthNP[asparagus[0], asparagus[1]]
            pcdata = np.array([1,1])
            spears.append(Spear(box = box, mask = mask,
                                 top_point = top_point, bot_point = bot_point,
                                 top_3d=top_point3d, bot_3d = bot_point3d,
                                 lenght = length, id = idx,
                                 pcdata = pcdata))


        return spears
