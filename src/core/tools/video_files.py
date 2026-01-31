#!/usr/bin/python3

import asyncio
import logging
import pathlib
from datetime import datetime

import src.core as core
import src.core.tools as tools


class VideoFile(core.WorkflowModuleBase):
    """ """

    def __init__(self, logger=None, logger_name="DefaultLogger"):
        """ """
        super().__init__(logger, logger_name)
        self.clear()

    def clear(self):
        """ """
        super().clear()

    def configure(self, config_dict):
        """ """
        super().configure(config_dict)
        p = config_dict.get("parameters", {})
        self.source_dir = p.get("source_dir", "./wirc_recordings/")
        self.path_glob_string = p.get("path_glob_string", "**/*.mp4")

    async def pre_process_data(self):
        """ """
        await super().pre_process_data()

    async def process_data(self, data_dict={}):
        """Put your algorithmic code here."""
        try:
            results = []
            source_path = pathlib.Path(self.source_dir)
            # Create empty source dir if not exists.
            if not source_path.exists():
                source_path.mkdir(parents=True)

            video_files = list(source_path.glob(self.path_glob_string))

            for video_file in video_files:
                if video_file:
                    results.append(str(video_file))
            self.logger.info("Video source dir: " + str(source_path.resolve()))
            self.logger.info("Number of video files found: " + str(len(results)))
            results.sort()

            for path in results:
                data_dict = {
                    "video_path": path,
                }
                await self.data_to_output_queues(data_dict, "video_path")

        except Exception as e:
            message = self.class_name + " - process_data. "
            message += "Exception: " + str(e)
            self.logger.error(message)

    async def post_process_data(self):
        """ """
        await super().post_process_data()

        # This tool is finished. No more data.
        await self.data_to_output_queues(None, "video_path")
