from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Streamer
from subs.AsparagusProcessor import AsparagusProcessor
from subs.Pather import Pather
from subs.Visualizer import Vizualizer
from subs.Communicator import Communicator

import cv2
import numpy as np
import traceback

output = Streamer(ip = '192.168.1.108', port = 5000)
camera = Camera()

# ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_asparagus/model.engine')
ep = EngineProcessor('/home/andrii/Gus2/networks/yolo2/model.engine')
prp = PreProcessor()
pop = PostProcessor(iou_threshold = 0.8, class_threshold = 0.85,
                 input_height = 480, input_width = 640, img_height = 480, img_width = 640,
                  num_masks = 32)

pather = Pather(min_lenght = 0, min_dist = 100000)
viz = Vizualizer()
coms = Communicator(False, False)

ep.initalize()
camera.initCamera()
output.initStreamer()
asparagusProcessor = AsparagusProcessor(topk = 0.06, botk = 0.06, camera = camera)
try:
    while True:


        camera.getData()
        image = camera.image
        image_data = prp.process(image)
        net_output = ep.process(image_data)
        boxes, masks, classid = pop.process(net_output)
        if len(classid) != 0:


            spears = asparagusProcessor.process(boxes, masks)
            for s in spears:
                print(s)
            stopSignal, spear, spear3d = pather.processSpears(spears)



            if len(spears) != 0:
                image = viz.process(image, spears)

        output.Render(image)

except Exception as e:
    traceback.print_exc()
    ep.deinitialize()
finally:
    ep.deinitialize()