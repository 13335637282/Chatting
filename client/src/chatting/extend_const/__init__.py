from enum import StrEnum, IntEnum,Enum


class HTTPStatusExtend(IntEnum):
    UNABLE_CONNECT_TO_SERVER = -1

class IntConst(IntEnum):
    CANNOT_LOAD_FONT = -1
    DEFAULT_FONT_SIZE = 12
    CUSTOM_FONT_FAMILY_INDEX = 0
    DEFAULT_FONT_FAMILY_INDEX = 0
    MESSAGES_FILE_INDENT = 2
    MAIN_WINDOW_MINIMUM_SIZE_W = 800
    MAIN_WINDOW_MINIMUM_SIZE_H = 600
    FRIENDS_REFRESH_TIMER = 10000
    MESSAGES_REFRESH_TIMER = 5000

class StringConst(StrEnum):
    DEFAULT_UPDATE_SERVER_URL = "http://127.0.0.1:5000/update"
    DEFAULT_SERVER_URL = "http://127.0.0.1:5000/api/v1"
    DEFAULT_FONT_PATH = r"./ChattingClientFile/font/SourceHan/Variable/TTF/SourceHanSansSC-VF.ttf"