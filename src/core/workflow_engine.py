#!/usr/bin/python3

import asyncio
import logging
import pathlib
import yaml
from datetime import datetime

import src.core as core
import src.core.steps as steps


class WorkflowEngine:
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
        self.config = None
        self.workflow_steps = []
        self.step_lookup = {}
        self.step_config = {}
        # Parameters.
        self.source_dir = "wirc_recordings"
        self.target_dir = "video_target"
        #

    def configure(self, parameters):
        """ """
        self.class_name = self.__class__.__name__
        p = parameters
        self.source_dir = p.get("source_dir", self.source_dir)
        self.target_dir = p.get("target_dir", self.target_dir)

    # def launch_startup(self, config_file):
    #     """ """
    #     loop = asyncio.get_event_loop()
    #     self.startup_task = asyncio.create_task(
    #         self.startup(config_file), name="Workflow startup."
    #     )
    #     asyncio.wait_for(self.startup_task, timeout=0)

    async def startup(self, config_file):
        """ """
        self.load_config(config_file)
        await asyncio.sleep(0)
        self.create_steps()
        await asyncio.sleep(0)
        self.config_steps()
        await asyncio.sleep(0)
        self.connect_steps()
        await asyncio.sleep(0)
        await self.execute_steps()
        await asyncio.sleep(0)
        #
        print("Done.")

    def load_config(self, config_file):
        """ """
        config_path = pathlib.Path(config_file)
        with open(config_path) as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
        #
        # print(self.config)
        self.configure(self.config.get("parameters", {}))

    def create_steps(self):
        """ """
        for step_dict in self.config.get("workflow", []):
            step_id = step_dict.get("step_id", "")
            self.workflow_steps.append(step_id)
            self.step_config[step_id] = step_dict
            algorithm = step_dict.get("algorithm", "")
            step_object = steps.step_factory(algorithm)
            if step_object != None:
                self.step_lookup[step_id] = step_object

    def config_steps(self):
        """ """
        for step_id in self.workflow_steps:
            step_dict = self.step_config[step_id]
            if step_id in self.step_lookup:
                self.step_lookup[step_id].configure(step_dict["parameters"])

    def connect_steps(self):
        """ """
        for step_id in self.workflow_steps:
            step_dict = self.step_config[step_id]
            if step_id in self.step_lookup:
                input_from = step_dict.get("input_from", "None")
                input_format = step_dict.get("input_format", "None")
                if input_from == "None":
                    continue
                input_queue = self.step_lookup[step_id].get_input_queue()
                self.step_lookup[input_from].add_output_queue(input_queue, input_format)

    async def execute_steps(self):
        """ """
        tasks = []
        for step_id in self.workflow_steps:
            step_dict = self.step_config[step_id]
            if step_id in self.step_lookup:
                task = await self.step_lookup[step_id].startup()
                tasks.append(task)
                await asyncio.sleep(0)
        # Wait until finished.
        await asyncio.wait(tasks)
        print("Tasks finished.")
