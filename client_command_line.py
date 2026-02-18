import argparse
import json
from typing import Any, Dict, List, Optional

import rich

from client_api import (accept_friend_request, get_friends_list,
                        get_incoming_requests, get_outgoing_requests, login,
                        logout, register, reject_friend_request, remove_friend,
                        send_friend_request)

# ========== 函数映射表（将字符串映射到实际函数） ==========
FUNCTIONS = {
    "register": register,
    "login": login,
    "logout": logout,
    "send_friend_request": send_friend_request,
    "get_incoming_requests": get_incoming_requests,
    "get_outgoing_requests": get_outgoing_requests,
    "accept_friend_request": accept_friend_request,
    "reject_friend_request": reject_friend_request,
    "get_friends_list": get_friends_list,
    "remove_friend": remove_friend,
}

# ========== 命令配置（数据与代码分离） ==========
# 配置格式：
# - id: 子命令名称
# - help: 帮助信息
# - function: (叶子命令) 对应的函数名，须在 FUNCTIONS 中定义
# - args: (叶子命令) 参数列表，每个参数包含 name（--长选项）, short（-短选项）, type, required, default, help
# - subcommands: (中间命令) 子命令列表
COMMANDS = [
    {
        "id": "register",
        "help": "注册新用户",
        "function": "register",
        "args": [
            {
                "name": "--username",
                "short": "-u",
                "type": str,
                "required": True,
                "help": "用户名",
            },
            {
                "name": "--password",
                "short": "-p",
                "type": str,
                "required": True,
                "help": "密码",
            },
        ],
    },
    {
        "id": "login",
        "help": "登录并获取 token",
        "function": "login",
        "args": [
            {
                "name": "--username",
                "short": "-u",
                "type": str,
                "required": True,
                "help": "用户名",
            },
            {
                "name": "--password",
                "short": "-p",
                "type": str,
                "required": True,
                "help": "密码",
            },
        ],
    },
    {
        "id": "logout",
        "help": "登出（删除 token）",
        "function": "logout",
        "args": [
            {
                "name": "--token",
                "short": "-t",
                "type": str,
                "required": True,
                "help": "身份令牌",
            },
        ],
    },
    {
        "id": "friend",
        "help": "好友相关操作",
        "subcommands": [
            {
                "id": "request",
                "help": "好友请求操作",
                "subcommands": [
                    {
                        "id": "send",
                        "help": "发送好友请求",
                        "function": "send_friend_request",
                        "args": [
                            {
                                "name": "--token",
                                "short": "-t",
                                "type": str,
                                "required": True,
                                "help": "身份令牌",
                            },
                            {
                                "name": "--friend-username",
                                "short": "-f",
                                "type": str,
                                "required": True,
                                "help": "对方用户名",
                            },
                            {
                                "name": "--message",
                                "short": "-m",
                                "type": str,
                                "required": False,
                                "default": "",
                                "help": "附加消息",
                            },
                        ],
                    },
                    {
                        "id": "incoming",
                        "help": "查看收到的好友请求",
                        "function": "get_incoming_requests",
                        "args": [
                            {
                                "name": "--token",
                                "short": "-t",
                                "type": str,
                                "required": True,
                                "help": "身份令牌",
                            },
                        ],
                    },
                    {
                        "id": "outgoing",
                        "help": "查看发出的好友请求",
                        "function": "get_outgoing_requests",
                        "args": [
                            {
                                "name": "--token",
                                "short": "-t",
                                "type": str,
                                "required": True,
                                "help": "身份令牌",
                            },
                        ],
                    },
                    {
                        "id": "accept",
                        "help": "接受好友请求",
                        "function": "accept_friend_request",
                        "args": [
                            {
                                "name": "--token",
                                "short": "-t",
                                "type": str,
                                "required": True,
                                "help": "身份令牌",
                            },
                            {
                                "name": "--request-id",
                                "short": "-r",
                                "type": int,
                                "required": True,
                                "help": "请求ID",
                            },
                        ],
                    },
                    {
                        "id": "reject",
                        "help": "拒绝好友请求",
                        "function": "reject_friend_request",
                        "args": [
                            {
                                "name": "--token",
                                "short": "-t",
                                "type": str,
                                "required": True,
                                "help": "身份令牌",
                            },
                            {
                                "name": "--request-id",
                                "short": "-r",
                                "type": int,
                                "required": True,
                                "help": "请求ID",
                            },
                        ],
                    },
                ],
            },
            {
                "id": "list",
                "help": "查看好友列表",
                "function": "get_friends_list",
                "args": [
                    {
                        "name": "--token",
                        "short": "-t",
                        "type": str,
                        "required": True,
                        "help": "身份令牌",
                    },
                ],
            },
            {
                "id": "remove",
                "help": "删除好友",
                "function": "remove_friend",
                "args": [
                    {
                        "name": "--token",
                        "short": "-t",
                        "type": str,
                        "required": True,
                        "help": "身份令牌",
                    },
                    {
                        "name": "--friend-id",
                        "short": "-f",
                        "type": int,
                        "required": True,
                        "help": "好友ID",
                    },
                ],
            },
        ],
    },
]


def build_parser(
    parser: argparse.ArgumentParser, commands: List[Dict[str, Any]]
) -> None:
    """
    递归构建 argparse 子命令解析器
    :param parser: 当前层级的解析器（将为其添加子命令）
    :param commands: 命令配置列表
    """
    # 为当前解析器添加子命令组（必须指定 dest 和 required）
    subparsers = parser.add_subparsers(title="子命令", dest="subcommand", required=True)

    for cmd in commands:
        cmd_parser = subparsers.add_parser(cmd["id"], help=cmd.get("help", ""))

        if "subcommands" in cmd:
            # 中间节点：递归添加下一级子命令
            build_parser(cmd_parser, cmd["subcommands"])
        else:
            # 叶子节点：添加参数并绑定处理函数
            for arg in cmd.get("args", []):
                # 构建选项名列表（长选项 + 短选项）
                option_strings = [arg["name"]]
                if "short" in arg:
                    option_strings.append(arg["short"])

                # 根据 required 和 default 添加参数
                if arg.get("required", False):
                    cmd_parser.add_argument(
                        *option_strings,
                        type=arg.get("type", str),
                        required=True,
                        help=arg.get("help", ""),
                    )
                else:
                    cmd_parser.add_argument(
                        *option_strings,
                        type=arg.get("type", str),
                        required=False,
                        default=arg.get("default"),
                        help=arg.get("help", ""),
                    )

            # 将处理函数保存在解析结果中
            cmd_parser.set_defaults(func=FUNCTIONS[cmd["function"]])


def print_response(resp) -> None:
    """尝试用 rich 美观地打印响应"""
    try:
        rich.inspect(resp)
        # 尝试打印 JSON 内容
        if hasattr(resp, "json") and callable(resp.json):
            try:
                data = resp.json()
                rich.print(data)
            except Exception:
                rich.print(f"状态码: {resp.status_code}, 响应体: {resp.text}")
        else:
            rich.print(resp)
    except Exception as e:
        rich.print(f"打印响应时出错: {e}")
        rich.print(resp)


if __name__ == "__main__":
    # 创建顶层解析器
    parser = argparse.ArgumentParser(description="聊天客户端调试工具（配置驱动）")
    build_parser(parser, COMMANDS)

    args = parser.parse_args()

    try:
        # 获取叶子命令绑定的处理函数
        func = args.func

        # 提取参数（过滤掉 argparse 内部添加的键）
        kwargs = {
            k: v for k, v in vars(args).items() if k not in ("func", "subcommand")
        }

        # 调用 API 函数
        response = func(**kwargs)

        # 打印结果
        print_response(response)

    except Exception as e:
        rich.print(f"[red]执行命令时发生异常: {e}[/red]")
