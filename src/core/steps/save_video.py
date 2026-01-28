#!/usr/bin/python3

import asyncio
import logging
import pathlib
import cv2
from datetime import datetime

import src.core as core
import src.core.steps as steps


class SaveVideo:
    """ """

    def __init__(self, logger=None, logger_name="DefaultLogger"):
        """ """
        self.logger = logger
        if self.logger == None:
            self.logger = logging.getLogger(logger_name)
        #
        self.class_name = self.__class__.__name__
        self.clear()
        # self.configure()

    def clear(self):
        """ """
        self.aaa = "A"
        self.input_from = "video_files"
        self.input_format = "video_frame"
        self.input_queue_size = 100
        # For a future base class.
        self.worker_task = None
        self.input_queue = None
        self.output_queues = []
        #
        self.video_out = None

    def configure(self, parameters):
        """ """
        p = parameters
        self.input_from = p.get("input_from", self.input_from)
        self.input_format = p.get("input_format", self.input_format)
        self.input_queue_size = p.get("input_queue_size", self.input_queue_size)
        # Create input queue.
        self.input_queue = asyncio.Queue(maxsize=self.input_queue_size)
        #
        # Background.
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        # Kernel for morphologyEx.
        kernel_size = (5, 5)
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

            if self.video_out == None:
                out_path = "./test_workflow_video.mp4"
                frame_width = 1456
                frame_height = 1088
                fps = 30
                # frame_width = 1280
                # frame_height = 800
                # fps = 30
                # frame_width = 256
                # frame_height = 384
                # fps = 25

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

    # Methods below for a future base class.

    def get_input_queue(self):
        """ """
        return self.input_queue

    async def startup(self):
        """ """
        try:
            # Read data from input queue.
            self.worker_task = asyncio.create_task(
                self._worker(), name="Step VideoFile."
            )
            return self.worker_task
        except Exception as e:
            message = self.class_name + " - startup. "
            message += "Exception: " + str(e)
            self.logger.error(message)

    async def shutdown(self):
        """ """
        try:
            self.capture_is_active = False
            if self.worker_task != None:
                self.worker_task.cancel()
                self.worker_task = None
        except Exception as e:
            message = self.class_name + " - shutdown. Exception: " + str(e)
            self.logger.error(message)

    async def _worker(self):
        """ """
        try:
            if self.input_queue == None:
                await self.process_data()
                return
            while True:
                try:
                    item = await self.input_queue.get()
                    try:
                        if item == None:
                            # Terminated by earlier workflow step.
                            break
                        # elif item == False:
                        #     continue
                        else:
                            await self.process_data(item)
                    finally:
                        self.input_queue.task_done()
                        await asyncio.sleep(0)

                except asyncio.CancelledError:
                    self.logger.error(self.class_name + " - Worker cancelled.")
                    break
                except Exception as e:
                    message = self.class_name + " - rec_target_worker(1): " + str(e)
                    self.logger.error(message)
                await asyncio.sleep(0)
        except Exception as e:
            message = self.class_name + " - rec_target_worker(2). Exception: " + str(e)
            self.logger.error(message)
        finally:
            self.logger.info(self.class_name + " - Worker ended.")

    def set_input_queue(self, queue, format):
        """ """
        self.input_queue = queue
        self.input_queue_format = format

    def add_output_queue(self, queue, format):
        """ """
        queue_dict = {
            "queue": queue,
            "format": format,
        }
        self.output_queues.append(queue_dict)

    async def data_to_output_queues(self, data_dict, format):
        """ """
        try:
            for output_queue_dict in self.output_queues:
                if output_queue_dict["format"] == format:
                    try:
                        queue = output_queue_dict["queue"]
                        await queue.put(data_dict)
                        # self.main_loop.call_soon_threadsafe(
                        #     output_queue.put,
                        #     data_dict,
                        # )
                    #
                    except Exception as e:
                        message = (
                            self.class_name + " - data_to_output_queues: " + str(e)
                        )
                        self.logger.info(message)
        except asyncio.QueueShutDown:
            message = self.class_name + " - data_to_output_queues: QueueShutDown."
            self.logger.info(message)
        except Exception as e:
            message = self.class_name + " - data_to_output_queues. Exception: " + str(e)
            self.logger.error(message)
