


class Spear:
    def __init__(self, box, mask, bot_point, top_point, top_3d, bot_3d, lenght, id):
        self.box = box
        self.mask = mask
        self.bot_point = bot_point
        self.top_point = top_point
        self.top_3d = top_3d
        self.bot_3d = bot_3d
        self.lenght = lenght
        self.id = id
        self.mid_point = (self.top_point + (self.bot_point - self.top_point)//2).astype(np.int)




    def __str__(self):
        return f'{"-"*60} \nSPEAR: \n ' \
               f'Bot point:{self.bot_3d}\t ' \
               f'Top point:{self.top_3d}\t' \
               f'Lenght   :{self.lenght}'


if __name__ == '__main__':
    a = [1,2,3]
    b = [4,5,6]
    for idx, (a1, b1) in enumerate(zip(a,b)):
        print(f'{idx} {a1} {b1}')