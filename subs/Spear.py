

import numpy as np
class Spear:
    def __init__(self, box, mask, bot_point, top_point, top_3d, bot_3d, lenght, id, skeleton, skeleton_3d, roll, pitch, yaw):
        self.box = box
        self.mask = mask
        self.bot_point = bot_point
        self.top_point = top_point
        self.top_3d = top_3d
        self.bot_3d = bot_3d
        self.lenght = lenght
        self.id = id
        self.skeleton = skeleton
        self.skeleton_3d = skeleton_3d
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def to_dict(self):
        mask_data = np.where(self.mask == 1)
        mask_data = [mask_data[0].tolist(), mask_data[1].tolist()]

        return {'box'       : self.box.tolist(),
                'mask'      : mask_data,
                'bot_point' : self.bot_point.tolist(),
                'top_point' : self.top_point.tolist(),
                'top_3d'    : self.top_3d.tolist(),
                'bot_3d'    : self.bot_3d.tolist(),
                'length'    : self.lenght,
                'id'        : self.id,
                'skeleton'  : self.skeleton,
                'skeleton3d': self.skeleton_3d,
                'roll'      :  self.roll,
                'pitch'     : self.pitch,
                'yaw'       : self.yaw}


    @classmethod
    def from_dict(cls, data):
        # Create an instance of the class from the dictionary data
        return cls(box = data['box'], mask = data['mask'], bot_point = data['bot_point'], top_point = data['top_point'],
                   top_3d = data['top_3d'], bot_3d = data['bot_3d'], lenght = data['lenght'], id = data['id'],
                   skeleton = data['skeleton'], skeleton_3d = data['skeleton3d'])



    def __str__(self):
        return f'{"-"*60} \nSPEAR: \n ' \
               f'Bot 3D: {self.bot_3d}\t Bot 2D: {self.bot_point} \n' \
               f'Top 3D: {self.top_3d}\t Top 2D: {self.top_point} \n' \
               f'Lenght   :{self.lenght}\n'





if __name__ == '__main__':
    a = [1,2,3]
    b = [4,5,6]
    for idx, (a1, b1) in enumerate(zip(a,b)):
        print(f'{idx} {a1} {b1}')