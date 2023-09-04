from yolo_inferencing.PostProcessor import PostProcessor
from yolo_inferencing.PreProcessor import PreProcessor
from yolo_inferencing.EngineProcessor import EngineProcessor

from subs.Camera import Camera
from subs.VideoInterface import Streamer
from subs.AsparagusProcessor import AsparagusProcessor
from subs.Pather import Pather
from subs.Visualizer import Vizualizer
from subs.Communicator import Communicator


import yaml



def assemble(config_path = 'config.yaml'):
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)


    yolo_weights_path = config['yolo']['weights_path']
    yolo_iou_threshold = config['yolo']['iou_threshold']
    yolo_class_threshold = config['yolo']['class_threshold']
    yolo_num_masks = config['yolo']['num_masks']
    yolo_input_height = config['yolo']['input_height']
    yolo_input_width = config['yolo']['input_width']
    yolo_img_height = config['yolo']['img_height']
    yolo_img_width = config['yolo']['img_width']

    working_area_ignore_distance = config['working_area']['ignore_distance']
    min_distance_w_no_angle_correction = config['working_area']['min_distance_w_no_angle_correction']
    max_reachable_distance = config['working_area']['max_reachable_distance']

    asparagus_topk = config['asparagus']['topk']
    asparagus_botk = config['asparagus']['botk']
    asparagus_n_skeletons = config['asparagus']['n_skeletons']
    asparagus_min_lenght = config['asparagus']['min_lenht']

    streamer_ip = config['streamer']['ip']
    streamer_port = config['streamer']['port']

    output = Streamer(ip=streamer_ip, port=streamer_port)
    camera = Camera()

    ep = EngineProcessor(yolo_weights_path)
    prp = PreProcessor()
    pop = PostProcessor(iou_threshold=yolo_iou_threshold, class_threshold=yolo_class_threshold,
                        input_height=yolo_input_height, input_width=yolo_input_width, img_height=yolo_img_height,
                        img_width=yolo_img_width,num_masks=yolo_num_masks)
    asparagusProcessor = AsparagusProcessor(topk=asparagus_topk, botk=asparagus_botk, camera=camera,
                                            n_skeletons=asparagus_n_skeletons, ignore_distance=working_area_ignore_distance)
    pather = Pather(min_lenght=asparagus_min_lenght, min_distance_w_no_angle_correction=min_distance_w_no_angle_correction,
                    max_reachable_distance=max_reachable_distance)
    viz = Vizualizer()
    coms = Communicator(nav_required=False, arm_required=True)
    coms.initComs()
    ep.initalize()
    camera.initCamera()
    output.initStreamer()


    return ep, prp, pop, asparagusProcessor, pather, viz, coms, camera, output



