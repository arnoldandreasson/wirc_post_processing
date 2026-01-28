#!/usr/bin/python3

import asyncio
import logging
import pathlib
from datetime import datetime

import src.core as core
import src.core.steps as steps


class VideoFile:
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
        self.source_dir = "./wirc_recordings/"
        self.path_glob_string = "**/rpi-cam0_*.mp4"
        # For a future base class.
        self.worker_task = None
        self.input_queue = None
        self.input_queue_format = None
        self.output_queues = []

    def configure(self, parameters):
        """ """
        p = parameters
        self.path_glob_string = p.get("path_glob_string", self.path_glob_string)

    async def process_data(self, data_dict={}):
        """Put your algorithmic code here."""
        try:
            results = []

            self.source_dir = self.source_dir
            source_path = pathlib.Path(self.source_dir)
            # Create empty source dir if not exists.
            if not source_path.exists():
                source_path.mkdir(parents=True)
                return results

            video_files = list(source_path.glob(self.path_glob_string))

            for video_file in video_files:
                if video_file:
                    results.append(str(video_file))
            self.logger.info("Video source dir: " + str(source_path.resolve()))
            self.logger.info("Number of video files found: " + str(len(results)))
            results.sort()

            for path in results:
                data_dict = {
                    "data": path,
                }
                await self.data_to_output_queues(data_dict, "video_path")
            # This step is finished. No more data.
            await self.data_to_output_queues(None, "video_path")
        except Exception as e:
            message = self.class_name + " - process_data. "
            message += "Exception: " + str(e)
            self.logger.error(message)

    # Methods below for a future base class.

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
                        elif item == False:
                            continue
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
                        self.logger.error(message)
        except asyncio.QueueShutDown:
            message = self.class_name + " - data_to_output_queues: QueueShutDown."
            self.logger.error(message)
        except Exception as e:
            message = self.class_name + " - data_to_output_queues. Exception: " + str(e)
            self.logger.error(message)
