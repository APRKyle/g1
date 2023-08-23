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
import time
output = Streamer(ip = '192.168.1.108', port = 5000)
camera = Camera()
pather = Pather(min_lenght=5, min_dist = 500000)
coms = Communicator(arm_required = True)

ep = EngineProcessor('/home/andrii/Gus2/networks/yolo2/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.6, class_threshold = 0.6,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)

coms.initComs()
ep.initalize()
camera.initCamera()
output.initStreamer()


ignore_distance = 500
botk = 0.01
topk = 0.01
end_effector_len = 100

def remove_outliers(data):

    Q1 = np.percentile(data, 25, axis=0)
    Q3 = np.percentile(data, 75, axis=0)
    IQR = Q3 - Q1
    threshold_multiplier = 1.5
    outlier_mask = (data < Q1 - threshold_multiplier * IQR) | (data > Q3 + threshold_multiplier * IQR)
    cleaned_data = data[~np.any(outlier_mask, axis=1)]

    return cleaned_data
def calculate_batch_3d(points):
    res = []
    for p in points:
        p3d = camera._calculatePix3D(p)
        if np.array_equal(p3d, np.array([0, 0, 0])):
            print(f'point  {p3d}   ignored')
        else:
            res.append(p3d.tolist())
    return res
def split_into_n_pices(n , indexes, topk, botk):

    dist = indexes[0].max() - indexes[0].min()
    step = dist//n
    c = indexes[0].min()
    res = []
    for i in range(n):
        part = indexes[:, np.logical_and(indexes[0] >=c, indexes[0] <= c + step)]

        mean = np.mean(part, axis = 1).astype(np.int)[::-1]
        res.append(mean)

        c = c + step
    res = remove_outliers(np.array(res))
    res = res.tolist()
    bot_part = indexes[:, indexes[0] > indexes[0].max() - dist * botk]
    top_part = indexes[:, indexes[0] < indexes[0].min() + dist * topk]
    bot_point = np.mean(bot_part, axis = 1).astype(np.int)[::-1]
    top_point = np.mean(top_part, axis = 1).astype(np.int)[::-1]
    return res, bot_point, top_point



def get_angles(data):
    centroid = np.mean(data, axis=0)
    translated_points = data - centroid
    covariance_matrix = np.cov(translated_points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    dominant_eigenvector = eigenvectors[:, np.argmax(eigenvalues)]
    dominant_eigenvector /= np.linalg.norm(dominant_eigenvector)
    pitch = np.arcsin(dominant_eigenvector[2])
    yaw = np.arctan2(dominant_eigenvector[1], dominant_eigenvector[0])
    roll = 0

    pitch_deg = np.degrees(pitch)
    yaw_deg = np.degrees(yaw)
    roll_deg = np.degrees(roll)
    return pitch_deg, yaw_deg, roll_deg




try:
    while True:

        coms._readSignalFromArm()
        camera.getData()
        image = camera.image
        image_data = prp.process(image)
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)
        spears = []
        data = {}
        if len(classid) != 0:
            efficient_spear2d = False
            stop_signal = None
            efficient_spear3d = None
            angle = None

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

                pitch_deg, yaw_deg, roll_deg = get_angles(np.array(skeleton3d))

                spear = Spear(box = box, mask = mask, bot_point = bot_point, top_point = top_point, top_3d = top_3d,
                      bot_3d = bot_3d, lenght = length, id = idx, skeleton = skeleton, skeleton_3d = skeleton3d,
                              roll = roll_deg, yaw = yaw_deg, pitch = pitch_deg)

                spears.append(spear)
                data[idx] = spear.to_dict()

                lin_dist = abs(top_3d[1] - bot_3d[1])

            for spear in spears:
                botArm = pather._transformIntoRobot(spear.bot_3d)
                distance = np.linalg.norm(botArm)

                if distance < pather.min_dist:
                    efficient_spear2d = efficient_spear2d
                    efficient_spear3d = botArm
                    stop_signal = True
                    angle = 90 - round(spear.pitch) * -1

                    if stop_signal and coms.ARM_IS_READY:

                        coms._sendCoordsAngle(efficient_spear3d, angle)
                        time.sleep(5)



        output.Render(image, data)

except Exception as e:
    traceback.print_exc()
    ep.deinitialize()
finally:
    ep.deinitialize()