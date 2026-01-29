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
        self.input_queue_size = 100

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
            video_file_path = data_dict.get("data", "")
            video_file_path = pathlib.Path(video_file_path)
            video_name = video_file_path.name
            self.logger.info("File: " + video_name)

            start_time = datetime.now()

            frame_index = 0
            # Video stream.
            capture = cv2.VideoCapture(video_file_path)
            # # Background.
            # backSub = cv2.createBackgroundSubtractorMOG2()
            # # Kernel for morphologyEx.
            # kernel_size = (5, 5)
            # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)

            if not capture.isOpened():
                self.logger.error("Error opening video file: " + video_file_path.name)
            else:
                while capture.isOpened():
                    # Capture frame-by-frame.
                    ret, frame_bgr = capture.read()
                    if frame_bgr is None:
                        break

                    data_dict = {
                        "frame": frame_bgr,
                        "frame_index": frame_index,
                        "video_name": video_name,
                    }
                    frame_index += 1

                    await self.data_to_output_queues(data_dict, "video_frame")

        except Exception as e:
            message = self.class_name + " - process_data. "
            message += "Exception: " + str(e)
            self.logger.error(message)

    async def post_process_data(self):
        """ """
        await super().post_process_data()

        # This tool is finished. No more data.
        await self.data_to_output_queues(None, "video_frame")
