#!/usr/bin/python3

import asyncio
import logging
import pathlib
import cv2
from datetime import datetime

import src.core as core
import src.core.tools as tools


class ReadVideo(core.WorkflowModuleBase):
    """ """

    def __init__(self, logger=None, logger_name="DefaultLogger"):
        """ """
        super().__init__(logger, logger_name)
        self.clear()

    def clear(self):
        """ """
        super().clear()
        self.capture = None

    def configure(self, config_dict):
        """ """
        super().configure(config_dict)
        p = config_dict.get("parameters", {})

    async def pre_process_data(self):
        """ """
        await super().pre_process_data()

    async def process_data(self, data_dict={}):
        """Put your algorithmic code here."""
        try:
            video_path = data_dict.get("video_path", None)
            if video_path == None:
                return
            video_path = pathlib.Path(video_path)
            video_name = video_path.name
            self.logger.info("File: " + video_name)

            # Video stream.
            frame_index = 0
            self.capture = cv2.VideoCapture(video_path)
            if not self.capture.isOpened():
                self.logger.error("Error opening video file: " + video_path.name)
            else:
                try:
                    frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
                    frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    video_fps = self.capture.get(cv2.CAP_PROP_FPS)
                    video_path_str = str(video_path)
                    while self.capture.isOpened():
                        # Capture frame-by-frame.
                        ret, frame_bgr = self.capture.read()
                        if not ret:
                            break
                        dataout_dict = {
                            "frame": frame_bgr,
                            "video_name": video_name,
                            "video_path": video_path_str,
                            "frame_width": frame_width,
                            "frame_height": frame_height,
                            "video_fps": video_fps,
                            "frame_index": frame_index,
                        }
                        frame_index += 1
                        await self.data_to_output_queues(dataout_dict, "video_frame")
                finally:
                    if self.capture:
                        self.capture.release()
                        self.capture = None

        except Exception as e:
            message = self.class_name + " - process_data. "
            message += "Exception: " + str(e)
            self.logger.error(message)

    async def post_process_data(self):
        """ """
        await super().post_process_data()

        # This tool is finished. No more data.
        await self.data_to_output_queues(None, "video_frame")
