import argparse

import rich

from client_api import (accept_friend_request, get_friends_list,
                        get_incoming_requests, get_outgoing_requests, login,
                        logout, register, reject_friend_request, remove_friend,
                        send_friend_request)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="聊天客户端调试工具")
    subparsers = parser.add_subparsers(title="子命令", dest="subcommand", required=True)

    # 注册
    register_parser = subparsers.add_parser("register", help="注册新用户")
    register_parser.add_argument(
        "-u", "--username", type=str, required=True, help="用户名"
    )
    register_parser.add_argument(
        "-p", "--password", type=str, required=True, help="密码"
    )

    # 登录
    login_parser = subparsers.add_parser("login", help="登录并获取 token")
    login_parser.add_argument(
        "-u", "--username", type=str, required=True, help="用户名"
    )
    login_parser.add_argument("-p", "--password", type=str, required=True, help="密码")

    # 登出
    logout_parser = subparsers.add_parser("logout", help="登出（删除 token）")
    logout_parser.add_argument(
        "-t", "--token", type=str, required=True, help="身份令牌"
    )

    # 发送好友请求
    send_friend_parser = subparsers.add_parser(
        "send-friend-request", help="发送好友请求"
    )
    send_friend_parser.add_argument(
        "-t", "--token", type=str, required=True, help="身份令牌"
    )
    send_friend_parser.add_argument(
        "-f", "--friend-username", type=str, required=True, help="目标用户名"
    )
    send_friend_parser.add_argument(
        "-m", "--message", type=str, default="", help="附加消息（可选）"
    )

    # 查看收到的好友请求
    incoming_parser = subparsers.add_parser(
        "incoming-requests", help="查看收到的好友请求"
    )
    incoming_parser.add_argument(
        "-t", "--token", type=str, required=True, help="身份令牌"
    )

    # 查看发出的好友请求
    outgoing_parser = subparsers.add_parser(
        "outgoing-requests", help="查看发出的好友请求"
    )
    outgoing_parser.add_argument(
        "-t", "--token", type=str, required=True, help="身份令牌"
    )

    # 接受好友请求
    accept_parser = subparsers.add_parser("accept-request", help="接受好友请求")
    accept_parser.add_argument(
        "-t", "--token", type=str, required=True, help="身份令牌"
    )
    accept_parser.add_argument(
        "-r", "--request-id", type=int, required=True, help="好友请求ID"
    )

    # 拒绝好友请求
    reject_parser = subparsers.add_parser("reject-request", help="拒绝好友请求")
    reject_parser.add_argument(
        "-t", "--token", type=str, required=True, help="身份令牌"
    )
    reject_parser.add_argument(
        "-r", "--request-id", type=int, required=True, help="好友请求ID"
    )

    # 获取好友列表
    friends_parser = subparsers.add_parser("friends", help="获取好友列表")
    friends_parser.add_argument(
        "-t", "--token", type=str, required=True, help="身份令牌"
    )

    # 删除好友
    remove_friend_parser = subparsers.add_parser("remove-friend", help="删除好友")
    remove_friend_parser.add_argument(
        "-t", "--token", type=str, required=True, help="身份令牌"
    )
    remove_friend_parser.add_argument(
        "-f", "--friend-id", type=int, required=True, help="好友ID（来自好友列表）"
    )

    args = parser.parse_args()

    # 根据子命令调用对应的 API 函数
    try:
        if args.subcommand == "register":
            resp = register(args.username, args.password)
        elif args.subcommand == "login":
            resp = login(args.username, args.password)
        elif args.subcommand == "logout":
            resp = logout(args.token)
        elif args.subcommand == "send-friend-request":
            resp = send_friend_request(args.token, args.friend_username, args.message)
        elif args.subcommand == "incoming-requests":
            resp = get_incoming_requests(args.token)
        elif args.subcommand == "outgoing-requests":
            resp = get_outgoing_requests(args.token)
        elif args.subcommand == "accept-request":
            resp = accept_friend_request(args.token, args.request_id)
        elif args.subcommand == "reject-request":
            resp = reject_friend_request(args.token, args.request_id)
        elif args.subcommand == "friends":
            resp = get_friends_list(args.token)
        elif args.subcommand == "remove-friend":
            resp = remove_friend(args.token, args.friend_id)
        else:
            # 理论上不会走到这里，因为 subparsers 有 required=True
            parser.print_help()
            exit(1)

        # 打印响应结果
        try:
            # 尝试用 rich 的 inspect 显示对象细节
            rich.inspect(resp)
            # 再尝试打印 JSON 内容（如果有）
            if hasattr(resp, "json") and callable(resp.json):
                try:
                    data = resp.json()
                    rich.print(data)
                except Exception:
                    # 如果 JSON 解析失败，可能响应体不是 JSON 格式
                    rich.print(f"状态码: {resp.status_code}, 响应体: {resp.text}")
            else:
                rich.print(resp)
        except Exception as e:
            rich.print(f"打印响应时出错: {e}")
            rich.print(resp)

    except Exception as e:
        rich.print(f"[red]执行命令时发生异常: {e}[/red]")
