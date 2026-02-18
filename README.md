# Chatting - 一个开源的聊天软件

<p align="left">
<a href="https://github.com/13335637282/Chatting/releases"><img alt="Version" title="Version" src="https://img.shields.io/github/v/release/13335637282/Chatting?label=Version&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPQoid2hpdGUiIGQ9Ik0xIDcuNzc1VjIuNzVDMSAxLjc4NCAxLjc4NCAxIDIuNzUgMWg1LjAyNWMuNDY0IDAgLjkxLjE4NCAxLjIzOC41MTNsNi4yNSA2LjI1YTEuNzUgMS43NSAwIDAgMSAwIDIuNDc0bC01LjAyNiA1LjAyNmExLjc1IDEuNzUgMCAwIDEtMi40NzQgMGwtNi4yNS02LjI1QTEuNzUyIDEuNzUyIDAgMCAxIDEgNy43NzVabTEuNSAwYzAgLjA2Ni4wMjYuMTMuMDczLjE3N2w2LjI1IDYuMjVhLjI1LjI1IDAgMCAwIC4zNTQgMGw1LjAyNS01LjAyNWEuMjUuMjUgMCAwIDAgMC0uMzU0bC02LjI1LTYuMjVhLjI1LjI1IDAgMCAwLS4xNzctLjA3M0gyLjc1YS4yNS4yNSAwIDAgMC0uMjUuMjVaTTYgNWExIDEgMCAxIDEgMCAyIDEgMSAwIDAgMSAwLTJaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/13335637282/Chatting/watchers"><img alt="Watchers" title="Watchers" src="https://img.shields.io/github/watchers/13335637282/Chatting?label=Watchers&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggMmMxLjk4MSAwIDMuNjcxLjk5MiA0LjkzMyAyLjA3OCAxLjI3IDEuMDkxIDIuMTg3IDIuMzQ1IDIuNjM3IDMuMDIzYTEuNjIgMS42MiAwIDAgMSAwIDEuNzk4Yy0uNDUuNjc4LTEuMzY3IDEuOTMyLTIuNjM3IDMuMDIzQzExLjY3IDEzLjAwOCA5Ljk4MSAxNCA4IDE0Yy0xLjk4MSAwLTMuNjcxLS45OTItNC45MzMtMi4wNzhDMS43OTcgMTAuODMuODggOS41NzYuNDMgOC44OThhMS42MiAxLjYyIDAgMCAxIDAtMS43OThjLjQ1LS42NzcgMS4zNjctMS45MzEgMi42MzctMy4wMjJDNC4zMyAyLjk5MiA2LjAxOSAyIDggMlpNMS42NzkgNy45MzJhLjEyLjEyIDAgMCAwIDAgLjEzNmMuNDExLjYyMiAxLjI0MSAxLjc1IDIuMzY2IDIuNzE3QzUuMTc2IDExLjc1OCA2LjUyNyAxMi41IDggMTIuNWMxLjQ3MyAwIDIuODI1LS43NDIgMy45NTUtMS43MTUgMS4xMjQtLjk2NyAxLjk1NC0yLjA5NiAyLjM2Ni0yLjcxN2EuMTIuMTIgMCAwIDAgMC0uMTM2Yy0uNDEyLS42MjEtMS4yNDItMS43NS0yLjM2Ni0yLjcxN0MxMC44MjQgNC4yNDIgOS40NzMgMy41IDggMy41Yy0xLjQ3MyAwLTIuODI1Ljc0Mi0zLjk1NSAxLjcxNS0xLjEyNC45NjctMS45NTQgMi4wOTYtMi4zNjYgMi43MTdaTTggMTBhMiAyIDAgMSAxLS4wMDEtMy45OTlBMiAyIDAgMCAxIDggMTBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/13335637282/Chatting/forks"><img alt="Forks" title="Forks" src="https://img.shields.io/github/forks/13335637282/Chatting?label=Forks&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTUgNS4zNzJ2Ljg3OGMwIC40MTQuMzM2Ljc1Ljc1Ljc1aDQuNWEuNzUuNzUgMCAwIDAgLjc1LS43NXYtLjg3OGEyLjI1IDIuMjUgMCAxIDEgMS41IDB2Ljg3OGEyLjI1IDIuMjUgMCAwIDEtMi4yNSAyLjI1aC0xLjV2Mi4xMjhhMi4yNTEgMi4yNTEgMCAxIDEtMS41IDBWOC41aC0xLjVBMi4yNSAyLjI1IDAgMCAxIDMuNSA2LjI1di0uODc4YTIuMjUgMi4yNSAwIDEgMSAxLjUgMFpNNSAzLjI1YS43NS43NSAwIDEgMC0xLjUgMCAuNzUuNzUgMCAwIDAgMS41IDBabTYuNzUuNzVhLjc1Ljc1IDAgMSAwIDAtMS41Ljc1Ljc1IDAgMCAwIDAgMS41Wm0tMyA4Ljc1YS43NS43NSAwIDEgMC0xLjUgMCAuNzUuNzUgMCAwIDAgMS41IDBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/13335637282/Chatting/stargazers"><img alt="Stars" title="Stars" src="https://img.shields.io/github/stars/13335637282/Chatting?label=Stars&color=gold&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggLjI1YS43NS43NSAwIDAgMSAuNjczLjQxOGwxLjg4MiAzLjgxNSA0LjIxLjYxMmEuNzUuNzUgMCAwIDEgLjQxNiAxLjI3OWwtMy4wNDYgMi45Ny43MTkgNC4xOTJhLjc1MS43NTEgMCAwIDEtMS4wODguNzkxTDggMTIuMzQ3bC0zLjc2NiAxLjk4YS43NS43NSAwIDAgMS0xLjA4OC0uNzlsLjcyLTQuMTk0TC44MTggNi4zNzRhLjc1Ljc1IDAgMCAxIC40MTYtMS4yOGw0LjIxLS42MTFMNy4zMjcuNjY4QS43NS43NSAwIDAgMSA4IC4yNVptMCAyLjQ0NUw2LjYxNSA1LjVhLjc1Ljc1IDAgMCAxLS41NjQuNDFsLTMuMDk3LjQ1IDIuMjQgMi4xODRhLjc1Ljc1IDAgMCAxIC4yMTYuNjY0bC0uNTI4IDMuMDg0IDIuNzY5LTEuNDU2YS43NS43NSAwIDAgMSAuNjk4IDBsMi43NyAxLjQ1Ni0uNTMtMy4wODRhLjc1Ljc1IDAgMCAxIC4yMTYtLjY2NGwyLjI0LTIuMTgzLTMuMDk2LS40NWEuNzUuNzUgMCAwIDEtLjU2NC0uNDFMOCAyLjY5NFoiPjwvcGF0aD48L3N2Zz4=" /></a>
<a href="https://github.com/13335637282/Chatting/issues"><img alt="Issues" title="Issues" src="https://img.shields.io/github/issues/13335637282/Chatting?label=Issues&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggOS41YTEuNSAxLjUgMCAxIDAgMC0zIDEuNSAxLjUgMCAwIDAgMCAzWiI+PC9wYXRoPjxwYXRoIGZpbGw9IndoaXRlIiBkPSJNOCAwYTggOCAwIDEgMSAwIDE2QTggOCAwIDAgMSA4IDBaTTEuNSA4YTYuNSA2LjUgMCAxIDAgMTMgMCA2LjUgNi41IDAgMCAwLTEzIDBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/13335637282/Chatting/pulls"><img alt="Pull Requests" title="Pull Requests" src="https://img.shields.io/github/issues-pr/13335637282/Chatting?label=Pull%20Requests&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTEuNSAzLjI1YTIuMjUgMi4yNSAwIDEgMSAzIDIuMTIydjUuMjU2YTIuMjUxIDIuMjUxIDAgMSAxLTEuNSAwVjUuMzcyQTIuMjUgMi4yNSAwIDAgMSAxLjUgMy4yNVptNS42NzctLjE3N0w5LjU3My42NzdBLjI1LjI1IDAgMCAxIDEwIC44NTRWMi41aDFBMi41IDIuNSAwIDAgMSAxMy41IDV2NS42MjhhMi4yNTEgMi4yNTEgMCAxIDEtMS41IDBWNWExIDEgMCAwIDAtMS0xaC0xdjEuNjQ2YS4yNS4yNSAwIDAgMS0uNDI3LjE3N0w3LjE3NyAzLjQyN2EuMjUuMjUgMCAwIDEgMC0uMzU0Wk0zLjc1IDIuNWEuNzUuNzUgMCAxIDAgMCAxLjUuNzUuNzUgMCAwIDAgMC0xLjVabTAgOS41YS43NS43NSAwIDEgMCAwIDEuNS43NS43NSAwIDAgMCAwLTEuNVptOC4yNS43NWEuNzUuNzUgMCAxIDAgMS41IDAgLjc1Ljc1IDAgMCAwLTEuNSAwWiI+PC9wYXRoPjwvc3ZnPg==" /></a>
<a href="https://github.com/13335637282/Chatting/discussions"><img alt="Discussions" title="Discussions" src="https://img.shields.io/github/discussions/13335637282/Chatting?label=Discussions&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTEuNzUgMWg4LjVjLjk2NiAwIDEuNzUuNzg0IDEuNzUgMS43NXY1LjVBMS43NSAxLjc1IDAgMCAxIDEwLjI1IDEwSDcuMDYxbC0yLjU3NCAyLjU3M0ExLjQ1OCAxLjQ1OCAwIDAgMSAyIDExLjU0M1YxMGgtLjI1QTEuNzUgMS43NSAwIDAgMSAwIDguMjV2LTUuNUMwIDEuNzg0Ljc4NCAxIDEuNzUgMVpNMS41IDIuNzV2NS41YzAgLjEzOC4xMTIuMjUuMjUuMjVoMWEuNzUuNzUgMCAwIDEgLjc1Ljc1djIuMTlsMi43Mi0yLjcyYS43NDkuNzQ5IDAgMCAxIC41My0uMjJoMy41YS4yNS4yNSAwIDAgMCAuMjUtLjI1di01LjVhLjI1LjI1IDAgMCAwLS4yNS0uMjVoLTguNWEuMjUuMjUgMCAwIDAtLjI1LjI1Wm0xMyAyYS4yNS4yNSAwIDAgMC0uMjUtLjI1aC0uNWEuNzUuNzUgMCAwIDEgMC0xLjVoLjVjLjk2NiAwIDEuNzUuNzg0IDEuNzUgMS43NXY1LjVBMS43NSAxLjc1IDAgMCAxIDE0LjI1IDEySDE0djEuNTQzYTEuNDU4IDEuNDU4IDAgMCAxLTIuNDg3IDEuMDNMOS4yMiAxMi4yOGEuNzQ5Ljc0OSAwIDAgMSAuMzI2LTEuMjc1Ljc0OS43NDkgMCAwIDEgLjczNC4yMTVsMi4yMiAyLjIydi0yLjE5YS43NS43NSAwIDAgMSAuNzUtLjc1aDFhLjI1LjI1IDAgMCAwIC4yNS0uMjVaIj48L3BhdGg+PC9zdmc+" /></a>
</p>

Chatting 是一个基于 maliang GUI 框架开发的轻量级聊天客户端，配合 Flask 后端实现用户认证与 Token 管理。所有密码在传输前均使用 RSA 公钥加密，服务端使用 Argon2 进行哈希存储，保障基础安全。

## 其他文档
[开发文档](DEVELOPMENT.md)
[致谢名单](CREDITS.md)
[贡献指南](CONTRIBUTING.md)
[版本命名](VERSIONING.md)

## ✨ 功能特性

### 已完成
- [x] 用户注册 / 登录
- [x] 服务端 Token 生成与维护
- [x] 好友系统（发送请求、接受/拒绝、好友列表管理）

### 待完善
- [ ] 私聊 / 群聊
- [ ] 消息撤回与引用
- [ ] 文件传输与表情包
- [ ] 语音 / 视频通话
- [ ] 群组管理
- [ ] 完善的 API 及权限控制

## 📦 安装

### 环境要求
- Python 3.8+
- pip

### 步骤
1. 克隆仓库
   ```bash
   git clone https://github.com/13335637282/Chatting.git
   cd Chatting
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 启动服务端（生成 RSA 密钥对）
   ```bash
   python server.py
   ```
   首次运行会在当前目录生成 `PRIVATE_KEY.chatting` 和 `PUBLIC_KEY.chatting`，同时自动创建以下数据库文件：
   - `login.db` - 存储用户信息
   - `friends.db` - 存储好友关系
   - `friend_requests.db` - 存储好友请求
   
   **注意**：`PRIVATE_KEY.chatting` 必须严格保密，仅保留在服务端。

4. 配置客户端
   - 将服务端生成的 `PUBLIC_KEY.chatting` 复制到客户端运行目录。
   - 修改 `client_api.py` 中的 `BASE_URL` 变量，指向你的服务端地址（格式 `http://your-server-ip:5000/api/v1` ）。

5. 运行客户端
   ```bash
   python client_ui.py
   ```
6.分发给其他人 
   将 `PUBLIC_KEY.chatting`

## 📄 许可证

本项目基于 [Apache License 2.0](LICENSE) 开源。  
使用本项目时，请保留原始版权声明及许可证文本。

## star history
<p align="center">
    <a href="https://star-history.com/#13335637282/Chatting&Date">
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=13335637282/Chatting&type=Date&theme=dark" />
            <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=13335637282/Chatting&type=Date" />
            <img src="https://api.star-history.com/svg?repos=13335637282/Chatting&type=Date" />
        </picture>
    </a>
</p>
