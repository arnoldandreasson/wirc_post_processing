import src.core as core

from src.core.steps.video_files import VideoFile
from src.core.steps.read_video import ReadVideo
from src.core.steps.process_frame import ProcessFrame
from src.core.steps.save_video import SaveVideo


def step_factory(algorithm):
    """ """
    step_object = None
    if algorithm == "VideoFiles":
        step_object = VideoFile(logger_name=core.logger_name)
    elif algorithm == "ReadVideo":
        step_object = ReadVideo(logger_name=core.logger_name)
    elif algorithm == "ProcessFrame":
        step_object = ProcessFrame(logger_name=core.logger_name)
    elif algorithm == "SaveVideo":
        step_object = SaveVideo(logger_name=core.logger_name)
    #
    return step_object
