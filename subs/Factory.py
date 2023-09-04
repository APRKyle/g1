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
    working_area_min_dist = config['working_area']['min_dist']
    working_area_max_distance = config['working_area']['max_distance']

    asparagus_topk = config['asparagus']['topk']
    asparagus_botk = config['asparagus']['botk']
    asparagus_n_skeletons = config['asparagus']['n_skeletons']
    asparagus_min_lenht = config['asparagus']['min_lenht']

    streamer_ip = config['streamer']['ip']
    streamer_port = config['streamer']['port']

    output = Streamer(ip='192.168.1.108', port=5000)
    camera = Camera()

    ep = EngineProcessor('/home/andrii/Gus2/networks/yolo_asparagus/model.engine')
    prp = PreProcessor()
    pop = PostProcessor(iou_threshold=0.8, class_threshold=0.85,
                        input_height=480, input_width=640, img_height=480, img_width=640,
                        num_masks=32)
    asparagusProcessor = AsparagusProcessor(topk=0.15, botk=0.09, camera=camera, n_skeletons=15, ignore_distance=400)
    pather = Pather(min_lenght=0, min_dist=0, max_distance=1000000)
    viz = Vizualizer()
    coms = Communicator(nav_required=False, arm_required=True)
    coms.initComs()
    ep.initalize()
    camera.initCamera()
    output.initStreamer()


    return ep, prp, pop, asparagusProcessor, pather, viz, coms, camera, output



