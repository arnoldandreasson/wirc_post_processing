#!/usr/bin/python3

import asyncio
import logging
import pathlib
from datetime import datetime
import cv2

import src.core as core
import src.core.tools as tools


class ProcessFrame(core.WorkflowModuleBase):
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

        # Background.
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        # Kernel for morphologyEx.
        kernel_size = (5, 5)
        kernel_size = (3, 3)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)

    async def process_data(self, data_dict={}):
        """Put your algorithmic code here."""
        try:
            if data_dict == False:
                print("DEBUG: False")
                return

            frame_bgr = data_dict.get("frame", None)
            frame_index = data_dict.get("frame_index", None)
            video_name = data_dict.get("video_name", None)

            # Apply background subtraction.
            frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
            foreground_mask_1 = self.backSub.apply(frame_gray)

            # Apply erosion and dilation.
            foreground_mask = cv2.morphologyEx(
                foreground_mask_1, cv2.MORPH_OPEN, self.kernel
            )

            # Search for contours.
            contours, hierarchy = cv2.findContours(
                foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            min_contour_area = 50
            max_contour_area = 500
            # min_contour_area = 500
            # max_contour_area = 5000
            large_contours = [
                cnt
                for cnt in contours
                if (cv2.contourArea(cnt) > min_contour_area)
                and (cv2.contourArea(cnt) < max_contour_area)
            ]

            if len(large_contours) > 0:

                frame_out = frame_bgr.copy()
                for cnt in large_contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    frame_out = cv2.rectangle(
                        frame_out, (x, y), (x + w, y + h), (0, 0, 200), 1
                    )

                data_dict = {
                    "frame": frame_out,
                    "frame_index": frame_index,
                    "video_name": video_name,
                }

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
