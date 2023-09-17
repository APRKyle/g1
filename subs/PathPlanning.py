import numpy as np



class BrutePlanner:
    def __init__(self, end_effector, min_angle = -90, max_angle = 90, resolution = 5):
        self.ef = end_effector
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.resolution = resolution

        start = np.mean([min_angle, max_angle]).astype(int)
        self.degrees = np.array([start], dtype=float)
        n = (max_angle - min_angle) // resolution
        step = resolution
        for i in range(n // 2):
            a = np.array([start - step, start + step], dtype=float)
            self.degrees = np.concatenate((self.degrees, a))
            step += resolution

    def _sort_spears(self, spears):
        sorting_key = lambda x: np.linalg.norm(x.arm_bot_3d - self.ef.blade)
        data = sorted(spears.spears, key=sorting_key)
        return data

    def process(self, data):
        data = [np.array([d.arm_bot_3d[0], d.arm_bot_3d[2], d.arm_bot_3d[1]] for d in data)] #swaping axis
        ideal_angle = None
        for spear_idx, target in enumerate(data):


            for idx_a, degree in enumerate(self.degrees):
                self.ef.goto(target, degree, 'pre')
                cut_points = np.linspace(self.ef.approach_line[0], self.ef.approach_line[-1])

                success = False
                for p in cut_points:
                    self.ef.goto(p, angle=degree, pivot_point='blade')

                    outside_idxs = self.ef.inside_test(data)

                    if len(outside_idxs) - 1 != 0:
                        success = False

                        break
                    else:
                        success = True
                        ideal_angle = self.ef.angle
                        continue
                if success:
                    return ideal_angle, target, spear_idx




if __name__ == '__main__':
    pass