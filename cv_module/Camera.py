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
    def __init__(self, imageHeight=480, imageWidth=640, fps=30):
        self.imageHeight = imageHeight
        self.imageWidth = imageWidth
        self.FPS = fps

    def initCamera(self):
        pipeline = rs.pipeline()
        config = rs.config()
        pipeline_wrapper = rs.pipeline_wrapper(pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        config.enable_stream(rs.stream.depth, self.imageWidth, self.imageHeight, rs.format.z16, self.FPS)
        config.enable_stream(rs.stream.color, self.imageWidth, self.imageHeight, rs.format.rgb8, self.FPS)
        profile = pipeline.start(config)

        align_to = rs.stream.color
        self.align = rs.align(align_to)

        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        self.pipeline = pipeline

    def getData(self):

        frame = self._getFrame()
        image = self._getImage(frame)
        depthRS, depthNP = self._getDepth(frame)
        return image, depthRS, depthNP

    def _getFrame(self):

        frame = self.pipeline.wait_for_frames()
        frame = self.align.process(frame)
        return frame

    def _calculatePix3D(self, pix, depthFrame):
        depth_intrin = depthFrame.profile.as_video_stream_profile().intrinsics
        depth = depthFrame.get_distance(pix[0], pix[1])
        coord = rs.rs2_deproject_pixel_to_point(depth_intrin, pix, depth)
        coord = list(map(lambda x: int(round(x, 3) * 1000), coord))
        return coord

    def _getImage(self, frame):

        image = frame.get_color_frame()
        image = np.asanyarray(image.get_data())
        return image

    def _getDepth(self, frame):

        depthRS = frame.get_depth_frame()
        depthNP = np.asanyarray(depthRS.get_data())

        return depthRS, depthNP


