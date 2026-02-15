#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
import inspect
import threading
from typing import Dict, Optional, Union, Pattern, Match, TextIO, Any, NoReturn

__license__ = """Apache License 2.0"""


class Logger:
    """
    文件日志记录器，支持自动模糊化 UUID 格式的令牌。
    日志仅写入文件，控制台无输出。
    日志格式：'[%(asctime)s/%(name)s %(levelname)s]%(filename)s.%(funcName)s(%(lineno)s):\n %(message)s'
    """
    _level_names: Dict[str, int] = {
        'ZERO': 0,
        'DEBUG': 10,
        'INFO': 20,
        'WARNING': 30,
        'ERROR': 40,
        'CRITICAL': 50
    }

    # UUID 正则表达式：8-4-4-4-12 的十六进制数字
    _uuid_pattern: Pattern[str] = re.compile(
        r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'
    )

    def __init__(
        self,
        name: str,
        logfile: str,
        level: Union[str, int] = 'INFO',
        fmt: Optional[str] = None,
        mask_tokens: bool = False
    ) -> None:
        """
        初始化日志器
        :param name: 日志器名称
        :param logfile: 日志文件路径
        :param level: 日志级别，可以是字符串或整数
        :param fmt: 自定义输出格式，默认使用指定的格式
        :param mask_tokens: 是否模糊化 UUID 令牌（默认 False）
        """
        self.name: str = name
        self.logfile: str = logfile
        self.level: int = self._get_level_int(level)
        self.format: str = fmt or '[%(asctime)s/%(name)s %(levelname)s]%(filename)s.%(funcName)s(%(lineno)s):\n %(message)s'
        self.mask_tokens: bool = mask_tokens
        self.lock: threading.Lock = threading.Lock()
        self.file_handler: Optional[TextIO] = None

    def _get_level_int(self, level: Union[str, int]) -> int:
        if isinstance(level, str):
            return self._level_names.get(level.upper(), 20)
        return level

    def _get_level_name(self, level: int) -> str:
        for name, val in self._level_names.items():
            if val == level:
                return name
        return 'INFO'

    def setLevel(self, level: Union[str, int]) -> None:
        """设置日志级别"""
        self.level = self._get_level_int(level)

    def _open_file(self) -> None:
        """打开日志文件，如果目录不存在则创建"""
        dirname: str = os.path.dirname(self.logfile)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        self.file_handler = open(self.logfile, 'a', encoding='utf-8')

    def _close_file(self) -> None:
        """关闭日志文件"""
        if hasattr(self, 'file_handler') and self.file_handler:
            self.file_handler.close()
            self.file_handler = None

    def _mask_uuid(self, match: Match[str]) -> str:
        """
        将匹配的 UUID 替换为模糊版本：前4位 + ****-****-****-**** + 后4位
        """
        uuid: str = match.group(0)
        # 确保长度足够（标准 UUID 长度为 36）
        if len(uuid) == 36:
            return uuid[:4] + '****-****-****-****' + uuid[-4:]
        return uuid  # 如果不匹配长度，原样返回（实际上不会发生）

    def _mask_sensitive(self, message: Any) -> str:
        """
        对消息中的敏感信息进行模糊化处理（目前仅处理 UUID）
        先将 message 转为字符串，再执行替换。
        """
        if not self.mask_tokens:
            return str(message)
        try:
            # 确保为字符串
            msg_str: str = str(message)
            return self._uuid_pattern.sub(self._mask_uuid, msg_str)
        except Exception:
            # 如果处理出错，返回原始字符串形式（避免干扰主程序）
            return str(message)

    def _format_record(self, levelname: str, msg: str) -> str:
        """
        格式化日志记录
        """
        frame: Optional[inspect.FrameInfo] = inspect.currentframe()  # type: ignore[assignment]
        try:
            # 回溯两层获取调用者的信息
            caller_frame = frame.f_back.f_back  # type: ignore
            filename: str = os.path.basename(caller_frame.f_code.co_filename)
            funcname: str = caller_frame.f_code.co_name
            lineno: int = caller_frame.f_lineno
        finally:
            del frame

        asctime: str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        record: Dict[str, Union[str, int]] = {
            'asctime': asctime,
            'name': self.name,
            'levelname': levelname,
            'filename': filename,
            'funcName': funcname,
            'lineno': lineno,
            'message': msg
        }
        return self.format % record

    def log(self, level: int, msg: Any, *args: Any, **kwargs: Any) -> None:
        """
        记录日志，如果级别达到要求则写入文件
        msg 可以是任意类型，最终会转为字符串。
        """
        if self.level <= level:
            levelname: str = self._get_level_name(level)

            # 构建最终的消息字符串
            try:
                if args:
                    # 使用 % 格式化（要求 msg 是字符串）
                    formatted_msg: str = msg % args
                else:
                    # 没有额外参数，直接转为字符串
                    formatted_msg = str(msg)
            except Exception:
                # 如果格式化失败，回退到简单的字符串拼接
                formatted_msg = f"{msg} {args}" if args else str(msg)

            # 模糊化敏感信息（如果启用）
            formatted_msg = self._mask_sensitive(formatted_msg)

            log_entry: str = self._format_record(levelname, formatted_msg)
            self._open_file()
            self._write(log_entry)
            self._close_file()

    def _write(self, log_entry: str) -> None:
        """线程安全地写入日志文件"""
        with self.lock:
            if self.file_handler:
                self.file_handler.write(log_entry + '\n')
                self.file_handler.flush()
    # 便捷方法
    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        self.log(10, msg, *args, **kwargs)

    def info(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        self.log(20, msg, *args, **kwargs)

    def warning(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        self.log(30, msg, *args, **kwargs)

    def warn(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        self.warning(msg, *args, **kwargs)

    def error(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        self.log(40, msg, *args, **kwargs)

    def critical(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        self.log(50, msg, *args, **kwargs)

    def exception(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        """
        记录异常信息，通常在 except 块中调用
        """
        exc_info = kwargs.get('exc_info', True)
        if exc_info:
            import traceback
            tb: str = traceback.format_exc()
            # 将异常栈附加到消息中
            msg = f"{msg}\n{tb}"
        self.error(msg, *args, **kwargs)

    def __del__(self) -> None:
        self._close_file()


# 使用示例（正确调用方式）
if __name__ == '__main__':
    log = Logger('myapp', 'test.log', level='DEBUG', mask_tokens=True)

    # 正确的调用：第一个参数是字符串，后续参数用于 % 格式化
    token = '288512b1-6526-413e-90fe-1af03e544826'
    log.debug('访问令牌: %s', token)   # 正确

    # 即使错误地传入元组，也能正常工作（自动转为字符串）
    log.debug(("[注册] test -> 状态 200, 响应: %s", token))  # 仍会输出一个元组的字符串表示，但其中的 token 会被模糊化
    # 更常见的错误：多了一层括号
    log.debug(("登录令牌: %s", token))  # 相当于传入了元组作为第一个参数，args 为空，我们会将其转为字符串并模糊化

    # 异常信息
    try:
        raise ValueError(f"无效 token: {token}")
    except Exception:
        log.exception('捕获到异常')

    print('日志已写入 test.log，UUID 已被模糊化，请查看。')