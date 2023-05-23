import numpy as np




class AsparagusProcessor:
    def __init__(self, topk = 0.06, botk = 0.06):
        self.topk = topk
        self.botk = botk


    def process(self, boxes, masks):
        spears = []
        for box, mask in zip(boxes, masks):
            # asparagus[0] - y
            # asparagus[1] - x
            asparagus = np.where(mask == 1)
            asparagus = np.array([asparagus[0], asparagus[1]])

            length = box[3] - box[1]
            bot_part = asparagus[:, asparagus[0] > box[3] - length * 0.06]
            bot_point = np.mean(bot_part, axis=1).astype(np.int)

            top_part = asparagus[:, asparagus[1] < box[0] + length * 0.06]
            top_point = np.mean(top_part, axis=1).astype(np.int)
            spears.append([bot_point, top_point])
            print(f'spears in processor: {spears}')
        return spears
