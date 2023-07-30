import cv2
import sys
import numpy as np
import serial
import jetson
import argparse

sys.path.append('/usr/local/lib/python3.6/pyrealsense2')
import pyrealsense2 as rs
import RPi.GPIO as GPIO


class Camera:
    def __init__(self, imageHeight=480, imageWidth=640, fps=30, dfps = 30):
        self.imageHeight = imageHeight
        self.imageWidth = imageWidth
        self.FPS = fps
        self.DepthFPS = dfps


    def initCamera(self):
        pipeline = rs.pipeline()
        config = rs.config()
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        config.enable_stream(rs.stream.depth, self.imageWidth, self.imageHeight, rs.format.z16, self.DepthFPS)
        config.enable_stream(rs.stream.color, self.imageWidth, self.imageHeight, rs.format.rgb8, self.FPS)
        profile = pipeline.start(config)

        align_to = rs.stream.color
        self.align = rs.align(align_to)

        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        self.pipeline = pipeline
        self.depthRS = None


        self.points = rs.pointcloud()

    def getData(self):

        frame = self._getFrame()
        self._getImage(frame)
        self._getDepth(frame)


    def _getFrame(self):

        frame = self.pipeline.wait_for_frames()
        frame = self.align.process(frame)
        return frame

    def _getImage(self, frame):

        self.imageRS = frame.get_color_frame()
        self.image = np.asanyarray(self.imageRS.get_data())


    def _getDepth(self, frame):

        self.depthRS = frame.get_depth_frame()
        self.depthNP = np.asanyarray(self.depthRS.get_data())

    def _calculatePix3D(self, pix):
        #Depth frame should be depthrs frame
        depth_intrin = self.depthRS.profile.as_video_stream_profile().intrinsics
        depth = self.depthRS.get_distance(pix[0], pix[1])
        coord = rs.rs2_deproject_pixel_to_point(depth_intrin, pix, depth)
        coord = np.array(list(map(lambda x: int(round(x, 3) * 1000), coord)))
        return coord

    def getPointCloud(self):
        #inefcient !! (computationally hard)
        self.points.map_to(self.imageRS)
        pointcloud_data = self.points.calculate(self.depthRS)
        vertices = np.asanyarray(pointcloud_data.get_vertices())
        vertices = np.array([list(item) for item in vertices])

        # Filter out invalid points (where z = 0)
        mask = vertices[:, 2] > 0
        valid_points = vertices[mask]
        return mask, valid_points







