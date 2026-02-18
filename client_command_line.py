import argparse
from typing import Any, Dict, List

import rich

from client_api import (accept_friend_request, get_friends_list,
                        get_incoming_requests, get_outgoing_requests, login,
                        logout, register, reject_friend_request, remove_friend,
                        send_friend_request)

# ========== 函数映射表 ==========
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
COMMANDS = [
    {
        "id": "register",
        "help": "注册新用户",
        "function": "register",
        "args": [
            {
                "name": "--username",
                "short": "-u",
                "dest": "username",
                "type": str,
                "required": True,
                "help": "用户名",
            },
            {
                "name": "--password",
                "short": "-p",
                "dest": "plain_password",
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
                "dest": "username",
                "type": str,
                "required": True,
                "help": "用户名",
            },
            {
                "name": "--password",
                "short": "-p",
                "dest": "plain_password",
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
                "dest": "token",
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
                                "dest": "token",
                                "type": str,
                                "required": True,
                                "help": "身份令牌",
                            },
                            {
                                "name": "--friend-username",
                                "short": "-f",
                                "dest": "friend_username",
                                "type": str,
                                "required": True,
                                "help": "对方用户名",
                            },
                            {
                                "name": "--message",
                                "short": "-m",
                                "dest": "message",
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
                                "dest": "token",
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
                                "dest": "token",
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
                                "dest": "token",
                                "type": str,
                                "required": True,
                                "help": "身份令牌",
                            },
                            {
                                "name": "--request-id",
                                "short": "-r",
                                "dest": "request_id",
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
                                "dest": "token",
                                "type": str,
                                "required": True,
                                "help": "身份令牌",
                            },
                            {
                                "name": "--request-id",
                                "short": "-r",
                                "dest": "request_id",
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
                        "dest": "token",
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
                        "dest": "token",
                        "type": str,
                        "required": True,
                        "help": "身份令牌",
                    },
                    {
                        "name": "--friend-id",
                        "short": "-f",
                        "dest": "friend_id",
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
    """递归构建 argparse 子命令解析器"""
    subparsers = parser.add_subparsers(title="子命令", dest="subcommand", required=True)

    for cmd in commands:
        cmd_parser = subparsers.add_parser(cmd["id"], help=cmd.get("help", ""))

        if "subcommands" in cmd:
            build_parser(cmd_parser, cmd["subcommands"])
        else:
            # 叶子命令：添加参数
            for arg in cmd.get("args", []):
                option_strings = [arg["name"]]
                if "short" in arg:
                    option_strings.append(arg["short"])

                add_kwargs = {
                    "type": arg.get("type", str),
                    "help": arg.get("help", ""),
                }
                if arg.get("required", False):
                    add_kwargs["required"] = True
                else:
                    add_kwargs["default"] = arg.get("default")
                if "dest" in arg:
                    add_kwargs["dest"] = arg["dest"]

                cmd_parser.add_argument(*option_strings, **add_kwargs)

            # 绑定处理函数
            cmd_parser.set_defaults(func=FUNCTIONS[cmd["function"]])


def print_response(resp) -> None:
    """尝试用 rich 美观地打印响应"""
    try:
        rich.inspect(resp)
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
    parser = argparse.ArgumentParser(description="聊天客户端调试工具（配置驱动）")
    build_parser(parser, COMMANDS)

    args = parser.parse_args()

    try:
        func = args.func
        # 提取参数（过滤掉内部字段）
        kwargs = {
            k: v for k, v in vars(args).items() if k not in ("func", "subcommand")
        }
        response = func(**kwargs)
        print_response(response)
    except Exception as e:
        rich.print(f"[red]执行命令时发生异常: {e}[/red]")
