#!/usr/bin/python3

import asyncio
import logging
import pathlib
import cv2
from datetime import datetime

import src.core as core
import src.core.tools as tools


class SaveVideo(core.WorkflowModuleBase):
    """ """

    def __init__(self, logger=None, logger_name="DefaultLogger"):
        """ """
        super().__init__(logger, logger_name)
        self.clear()

    def clear(self):
        """ """
        super().clear()
        self.input_queue_size = 100
        #
        self.video_out = None

    def configure(self, config_dict):
        """ """
        p = config_dict.get("parameters", {})
        # Create input queue.
        self.input_queue_size = config_dict.get(
            "input_queue_size", self.input_queue_size
        )
        self.input_queue = asyncio.Queue(maxsize=self.input_queue_size)
        #
        # Background.
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        # Kernel for morphologyEx.
        kernel_size = (5, 5)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)

    async def pre_process_data(self):
        """ """
        await super().pre_process_data()

    async def process_data(self, data_dict={}):
        """Put your algorithmic code here."""
        try:
            if data_dict == False:
                print("DEBUG: False")
                return

            frame_bgr = data_dict.get("frame", None)
            frame_index = data_dict.get("frame_index", None)
            video_name = data_dict.get("video_name", None)

            if self.video_out == None:
                out_path = "./test_workflow_video.mp4"
                # frame_width = 1456
                # frame_height = 1088
                # fps = 30
                # frame_width = 1280
                # frame_height = 800
                # fps = 30
                frame_width = 256
                frame_height = 384
                fps = 25

                fourcc = cv2.VideoWriter_fourcc(*"avc1")  # AVC1 is equal to H.264.
                self.video_out = cv2.VideoWriter(
                    out_path,
                    fourcc,
                    fps,
                    (frame_width, frame_height),
                )

            self.video_out.write(frame_bgr)

            # finally:
            #     if self.video_out:
            #         self.video_out.release()

        except Exception as e:
            message = self.class_name + " - process_data. "
            message += "Exception: " + str(e)
            self.logger.error(message)

    async def post_process_data(self):
        """ """
        await super().post_process_data()
