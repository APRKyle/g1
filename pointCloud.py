from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Streamer
from subs.AsparagusProcessor import AsparagusProcessor
from subs.Pather import Pather
from subs.Visualizer import Vizualizer
from subs.Communicator import Communicator
from subs.Spear import Spear

import cv2
import numpy as np
import traceback

# output = Streamer(ip = '192.168.1.232', port = 5000)
camera = Camera()
pather = Pather(min_lenght=5, min_dist = 5)

ep = EngineProcessor('/home/andrii/Gus2/networks/yolo2/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.8, class_threshold = 0.85,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)


ep.initalize()
camera.initCamera()
# output.initStreamer()


ignore_distance = 500
botk = 0.01
topk = 0.01
end_effector_len = 100


def calculate_batch_3d(points):
    res = []
    for p in points:
        res.append(camera._calculatePix3D(p).tolist())
    return res
def split_into_n_pices(n , indexes, topk, botk):

    dist = indexes[0].max() - indexes[0].min()
    step = dist//n
    c = indexes[0].min()
    res = []
    for i in range(n):
        part = indexes[:, np.logical_and(indexes[0] >=c, indexes[0] <= c + step)]
        res.append(np.mean(part, axis = 1).astype(np.int)[::-1])
        c = c + step

    bot_part = indexes[:, indexes[0] > indexes[0].max() - dist * botk]
    top_part = indexes[:, indexes[0] < indexes[0].min() + dist * topk]
    bot_point = np.mean(bot_part, axis = 1).astype(np.int)[::-1]
    top_point = np.mean(top_part, axis = 1).astype(np.int)[::-1]
    return res, bot_point, top_point


try:
    while True:


        camera.getData()
        image = camera.image
        image_data = prp.process(image)
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)
        spears = []
        data = {}
        if len(classid) != 0:


            for idx, (box, mask) in enumerate(zip(boxes, masks)):

                mask[np.logical_and(mask == 1, camera.depthNP == 0)] = 0  # stereo dispaired pixels distance check
                mask[np.logical_and(mask == 1, camera.depthNP > ignore_distance)] = 0  # unreachable pixel ignorance


                if np.all(np.all(mask == 0)):
                    continue

                mask = mask.astype(np.int)
                asparagusMask = np.where(mask == 1)
                asparagus = np.array([asparagusMask[0], asparagusMask[1]])
                # asparagus: 0 -  y coordinate, 1 - x coordinate


                skeleton, bot_point, top_point = split_into_n_pices(20, asparagus, topk, botk)
                skeleton3d = calculate_batch_3d(skeleton)
                top_3d = camera._calculatePix3D(top_point)
                bot_3d = camera._calculatePix3D(bot_point)
                length = np.linalg.norm(bot_3d - top_3d)

                spear = Spear(box = box, mask = mask, bot_point = bot_point, top_point = top_point, top_3d = top_3d,
                      bot_3d = bot_3d, lenght = length, id = idx, skeleton = skeleton, skeleton_3d = skeleton3d)

                print(spear.to_dict())
                data[idx] = spear.to_dict()





                lin_dist = abs(top_3d[1] - bot_3d[1])

                if lin_dist > 130:
                    image[asparagus[0], asparagus[1], 1] = 255
                else:
                    image[asparagus[0], asparagus[1], 0] = 255

            # if len(spears) != 0:
            #     robot_skeleton = []
            #     for spear in spears:
            #         robot_skeleton = []
            #         for point in spear.skeleton_3d:
            #             robot_skeleton.append(pather._transformIntoRobot(point))
            #
            #         botArm = pather._transformIntoRobot(spear.bot_3d)
            #         endEndeffector = botArm + end_effector_len
            #         robot_skeleton_np = np.array(robot_skeleton)
            #         end_skeleton = robot_skeleton_np[robot_skeleton_np[:,1] > endEndeffector]




        # output.Render(image, data)

except Exception as e:
    traceback.print_exc()
    ep.deinitialize()
finally:
    ep.deinitialize()