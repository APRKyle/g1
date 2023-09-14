import numpy as np



class BrutePlanner:
    def __init__(self, end_effector, min_angle = -90, max_angle = 90, resolution = 5):
        self.ef = end_effector
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.resolution = resolution
        self.n_steps = np.ceil((max_angle - min_angle) / resolution).astype(int)

    def _sort_spears(self, spears):
        sorting_key = lambda x: np.linalg.norm(x.arm_bot_3d - self.ef.blade)
        data = sorted(spears.spears, key=sorting_key)
        return data

    def process(self, data):
        success = False
        ideal_angle = 0

        for spear_idx, spear_target in enumerate(data):
            target = spear_target.arm_bot_3d
            self.ef.goto(target, self.min_angle, 'pre')
            b_idx = spear_idx

            for _ in range(self.n_steps):
                success = False
                collisions = [False for i in range(len(data))]
                self.ef.goto(target, self.resolution, 'pre')
                cut_points = np.linspace(self.ef.approach_line[0], self.ef.approach_line[-1])

                for p in cut_points:
                    self.ef.goto(p, pivot_point='blade')

                    for idx, spear in enumerate(data):
                        if idx == b_idx:
                            continue
                        else:
                            collisions[idx] = self.ef.check_colision(spear.arm_bot_3d)

                    if any(collisions):
                        break
                    else:
                        pass
                if not any(collisions):
                    success = True
                    ideal_angle = self.ef.angle
                    best_idx = spear_idx
                    break
                else:
                    ideal_angle = None
        if success:
            return ideal_angle, target, best_idx

        else:
            return None, None, None


if __name__ == '__main__':
    pass