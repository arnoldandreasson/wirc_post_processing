from src.core.steps.video_files import VideoFile
from src.core.steps.read_video import ReadVideo
from src.core.steps.process_frame import ProcessFrame
from src.core.steps.save_video import SaveVideo


def step_factory(algorithm):
    """ """
    step_object = None
    if algorithm == "VideoFiles":
        step_object = VideoFile()
    elif algorithm == "ReadVideo":
        step_object = ReadVideo()
    elif algorithm == "ProcessFrame":
        step_object = ProcessFrame()
    elif algorithm == "SaveVideo":
        step_object = SaveVideo()
    #
    return step_object
