

import numpy as np
class Spear:
    def __init__(self, box, mask, bot_point, top_point, top_3d, bot_3d, lenght, id, skeleton, skeleton3d):
        self.box = box
        self.mask = mask
        self.bot_point = bot_point
        self.top_point = top_point
        self.top_3d = top_3d
        self.bot_3d = bot_3d
        self.lenght = lenght
        self.id = id
        self.skeleton = skeleton
        self.skeleton_3d = skeleton3d



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