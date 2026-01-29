import src.core as core

from src.core.tools.video_files import VideoFile
from src.core.tools.read_video import ReadVideo
from src.core.tools.process_frame import ProcessFrame
from src.core.tools.save_video import SaveVideo


def tool_factory(tool):
    """ """
    tool_object = None
    if tool == "VideoFiles":
        tool_object = VideoFile(logger_name=core.logger_name)
    elif tool == "ReadVideo":
        tool_object = ReadVideo(logger_name=core.logger_name)
    elif tool == "ProcessFrame":
        tool_object = ProcessFrame(logger_name=core.logger_name)
    elif tool == "SaveVideo":
        tool_object = SaveVideo(logger_name=core.logger_name)
    #
    return tool_object
