import src.core as core

from src.core.tools.source_files import SourceFiles
from src.core.tools.read_video import ReadVideo
from src.core.tools.frame_scanner import FrameScanner
from src.core.tools.save_video import SaveVideo


def tool_factory(tool):
    """ """
    tool_object = None
    if tool == "SourceFiles":
        tool_object = SourceFiles(logger_name=core.logger_name)
    elif tool == "ReadVideo":
        tool_object = ReadVideo(logger_name=core.logger_name)
    elif tool == "FrameScanner":
        tool_object = FrameScanner(logger_name=core.logger_name)
    elif tool == "SaveVideo":
        tool_object = SaveVideo(logger_name=core.logger_name)
    #
    return tool_object
