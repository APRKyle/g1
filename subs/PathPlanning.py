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
        sorting_key = lambda x: np.linalg.norm(x.arm_bot_3d_2 - self.ef.blade)
        data = sorted(spears, key=sorting_key)
        return data

    def process(self, data):
        data = self._sort_spears(data)
        data = [i.arm_bot_3d_2 for i in data]
        if len(data) == 1:
            return 0, np.array([data[0], data[2], data[1]]), 0
        ideal_angle = None
        real_target = None
        b_idx = None
        success = False
        for spear_idx, spear_target in enumerate(data):
            target = spear_target

            if success:
                break

            for idx_a, degree in enumerate(self.degrees):
                self.ef.goto(target, degree, 'pre')
                cut_points = np.linspace(self.ef.approach_line[0], self.ef.approach_line[-1])
                if success:
                    break

                for p in cut_points:
                    self.ef.goto(p, angle=degree, pivot_point='blade')

                    outside_idxs = self.ef.inside_test(data)
                    print(data)
                    print(f'outside_idx: {outside_idxs}')
                    print(f'len: {len(outside_idxs)}')

                    if len(outside_idxs) - 1 != 0:
                        success = False
                        break
                    else:
                        success = True
                        ideal_angle = self.ef.angle
                        real_target = np.array([target[0], target[2], target[1]])
                        b_idx = spear_idx
                        continue

        return ideal_angle, real_target, b_idx


if __name__ == '__main__':
    pass