import argparse
from typing import Any, Dict, List

import rich

from client_api import (accept_friend_request, get_friends_list,
                        get_incoming_requests, get_outgoing_requests,
                        get_user_info, login, logout, register,
                        reject_friend_request, remove_friend, rename_user,
                        search_users, send_friend_request, update_user_profile)

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
    "get_user_info": get_user_info,
    "update_user_profile": update_user_profile,
    "rename_user": rename_user,
    "search_users": search_users,
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
        "id": "user",
        "help": "用户相关操作",
        "subcommands": [
            {
                "id": "info",
                "help": "获取用户详细信息",
                "function": "get_user_info",
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
                        "name": "--username",
                        "short": "-u",
                        "dest": "username",
                        "type": str,
                        "required": True,
                        "help": "要查询的用户名",
                    },
                ],
            },
            {
                "id": "profile",
                "help": "更新个人资料",
                "function": "update_user_profile",
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
                        "name": "--username",
                        "short": "-u",
                        "dest": "username",
                        "type": str,
                        "required": True,
                        "help": "要更新资料的用户名（必须是自己）",
                    },
                    {
                        "name": "--nickname",
                        "dest": "nickname",
                        "type": str,
                        "required": False,
                        "help": "昵称",
                    },
                    {
                        "name": "--birthday",
                        "dest": "birthday",
                        "type": str,
                        "required": False,
                        "help": "生日 (YYYY-MM-DD)",
                    },
                    {
                        "name": "--gender",
                        "dest": "gender",
                        "type": str,
                        "required": False,
                        "choices": ["male", "female", "other"],
                        "help": "性别",
                    },
                    {
                        "name": "--avatar",
                        "dest": "avatar",
                        "type": str,
                        "required": False,
                        "help": "头像 (base64编码)",
                    },
                    {
                        "name": "--email",
                        "dest": "email",
                        "type": str,
                        "required": False,
                        "help": "邮箱",
                    },
                    {
                        "name": "--phone",
                        "dest": "phone",
                        "type": str,
                        "required": False,
                        "help": "电话",
                    },
                    {
                        "name": "--bio",
                        "dest": "bio",
                        "type": str,
                        "required": False,
                        "help": "个人简介",
                    },
                ],
            },
            {
                "id": "rename",
                "help": "修改用户名",
                "function": "rename_user",
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
                        "name": "--old-username",
                        "short": "-o",
                        "dest": "old_username",
                        "type": str,
                        "required": True,
                        "help": "当前用户名",
                    },
                    {
                        "name": "--new-username",
                        "short": "-n",
                        "dest": "new_username",
                        "type": str,
                        "required": True,
                        "help": "新用户名 (至少3个字符)",
                    },
                ],
            },
            {
                "id": "search",
                "help": "搜索用户",
                "function": "search_users",
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
                        "name": "--query",
                        "short": "-q",
                        "dest": "query",
                        "type": str,
                        "required": True,
                        "help": "搜索关键词 (至少2个字符)",
                    },
                ],
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
                        "name": "--friend-username",
                        "short": "-f",
                        "dest": "friend_username",
                        "type": str,
                        "required": True,
                        "help": "好友用户名",
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
                if "choices" in arg:
                    add_kwargs["choices"] = arg["choices"]
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
        if hasattr(resp, "json") and callable(resp.json):
            try:
                data = resp.json()
                if resp.status_code == 200:
                    rich.print("[green]成功:[/green]")
                else:
                    rich.print(f"[red]错误 (状态码 {resp.status_code}):[/red]")
                rich.print(data)
            except Exception:
                if resp.status_code == 200:
                    rich.print("[green]成功:[/green]")
                else:
                    rich.print(f"[red]错误 (状态码 {resp.status_code}):[/red]")
                rich.print(f"响应体: {resp.text}")
        else:
            rich.print(resp)
    except Exception as e:
        rich.print(f"[red]打印响应时出错: {e}[/red]")
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
        # 过滤掉值为None的参数（未提供的可选参数）
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        response = func(**kwargs)
        print_response(response)
    except Exception as e:
        rich.print(f"[red]执行命令时发生异常: {e}[/red]")
