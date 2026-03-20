
# Chatting - 一个开源的聊天软件

<p align="left">
<a href="https://github.com/13335637282/Chatting/releases"><img alt="Version" title="Version" src="https://img.shields.io/github/v/release/13335637282/Chatting?label=Version&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTEgNy43NzVWMi43NUMxIDEuNzg0IDEuNzg0IDEgMi43NSAxSDcuNzc1Yy40NjQgMCAuOTEuMTg0IDEuMjM4LjUxM2w2LjI1IDYuMjVhMS43NSAxLjc1IDAgMCAxIDAgMi40NzRsLTUuMDI2IDUuMDI2YTEuNzUgMS43NSAwIDAgMS0yLjQ3NCAwbC02LjI1LTYuMjVBMS43NTIgMS43NTIgMCAwIDEgMSA3Ljc3NVptMS41IDBjMCAuMDY2LjAyNi4xMyAuMDczLjE3N2w2LjI1IDYuMjVhLjI1LjI1IDAgMCAwIC4zNTQgMGw1LjAyNS01LjAyNWEuMjUuMjUgMCAwIDAgMC0uMzU0bC02LjI1LTYuMjVhLjI1LjI1IDAgMCAwLS4xNzctLjA3M0gyLjc1YS4yNS4yNSAwIDAgMC0uMjUuMjVaTTYgNWExIDEgMCAxIDEgMCAyIDEgMSAwIDAgMSAwLTJaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/13335637282/Chatting/watchers"><img alt="Watchers" title="Watchers" src="https://img.shields.io/github/watchers/13335637282/Chatting?label=Watchers&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggMmMxLjk4MSAwIDMuNjcxLjk5MiA0LjkzMyAyLjA3OCAxLjI3IDEuMDkxIDIuMTg3IDIuMzQ1IDIuNjM3IDMuMDIzYTEuNjIgMS42MiAwIDAgMSAwIDEuNzk4Yy0uNDUuNjc4LTEuMzY3IDEuOTMyLTIuNjM3IDMuMDIzQzExLjY3IDEzLjAwOCA5Ljk4MSAxNCA4IDE0QzYuMDE5IDE0IDQuMzcxIDEzLjAwOCAzLjA2NyAxMS45MjJDMS43OTcgMTAuODMgLjg4IDkuNTc2IC40MyA4Ljg5OGExLjYyIDEuNjIgMCAwIDEgMC0xLjc5OGMuNDUtLjY3NyAxLjM2Ny0xLjkzMSAyLjYzNy0zLjAyMkM0LjMzIDIuOTkyIDYuMDE5IDIgOCAyWk0xLjY3OSA3LjkzMmEuMTIuMTIgMCAwIDAgMCAuMTM2Yy0uNDExLjYyMi0xLjI0MSAxLjc1LTIuMzY2IDIuNzE3QzUuMTc2IDExLjc1OCA2LjUyNyAxMi41IDggMTIuNWMxLjQ3MyAwIDIuODI1LS43NDIgMy45NTUtMS43MTUgMS4xMjQtLjk2NyAxLjk1NC0yLjA5NiAyLjM2Ni0yLjcxN2EuMTIuMTIgMCAwIDAgMC0uMTM2Yy0uNDEyLS42MjEtMS4yNDItMS43NS0yLjM2Ni0yLjcxN0MxMC44MjQgNC4yNDIgOS40NzMgMy41IDggMy41Yy0xLjQ3MyAwLTIuODI1Ljc0Mi0zLjk1NSAxLjcxNS0xLjEyNC45NjctMS45NTQgMi4wOTYtMi4zNjYgMi43MTdaTTggMTBhMiAyIDAgMSAxLS4wMDEtMy45OTlBMiAyIDAgMCAxIDggMTBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/13335637282/Chatting/forks"><img alt="Forks" title="Forks" src="https://img.shields.io/github/forks/13335637282/Chatting?label=Forks&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTUgNS4zNzJ2Ljg3OGMwIC40MTQuMzM2Ljc1Ljc1Ljc1aDQuNWEuNzUuNzUgMCAwIDAgLjc1LS43NXYtLjg3OGEyLjI1IDIuMjUgMCAxIDEgMS41IDB2Ljg3OGEyLjI1IDIuMjUgMCAwIDEtMi4yNSAyLjI1aC0xLjV2Mi4xMjhhMi4yNTEgMi4yNTEgMCAxIDEtMS41IDBWOC41aC0xLjVBMi4yNSAyLjI1IDAgMCAxIDMuNSA2LjI1di0uODc4YTIuMjUgMi4yNSAwIDEgMSAxLjUgMFpNNSAzLjI1YS43NS43NSAwIDEgMC0xLjUgMCAuNzUuNzUgMCAwIDAgMS41IDBabTYuNzUuNzVhLjc1Ljc1IDAgMSAwIDAtMS41Ljc1Ljc1IDAgMCAwIDAgMS41Wm0tMyA4Ljc1YS43NS43NSAwIDEgMC0xLjUgMCAuNzUuNzUgMCAwIDAgMS41IDBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/13335637282/Chatting/stargazers"><img alt="Stars" title="Stars" src="https://img.shields.io/github/stars/13335637282/Chatting?label=Stars&color=gold&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggLjI1QS43NS43NSAwIDAgMSA4LjY3My42MThMOS41NTIgNC40MzNsNC4yMS42MTJhLjc1Ljc1IDAgMCAxIC40MTYgMS4yNzlsLTMuMDQ2IDIuOTcuNzE5IDQuMTkyYS43NTEuNzUxIDAgMCAxLTEuMDg4Ljc5MUw4IDEyLjM0N2wtMy43NjYgMS45OEEuNzUuNzUgMCAwIDEgMy4xNDYgMTQuNWwtLjUyOC0zLjA4NC0zLjA5Ny0yLjk3YS43NS43NSAwIDAgMSAuNDE2LTEuMjhsNC4yMS0uNjExTDcuMzI3LjY2OEEuNzUuNzUgMCAwIDEgOCAuMjVabTAgMi40NDVMNi42MTUgNS41QS43NS43NSAwIDAgMSA2LjA1MSA1LjkxTDIuOTU0IDYuMzYgNS4xOTQgOC41NEEuNzUuNzUgMCAwIDEgNS40MSA5LjIwNGwtLjUyOCAzLjA4NCAyLjc2OS0xLjQ1NkEuNzUuNzUgMCAwIDEgOCAxMC43NWwyLjc3IDEuNDU2LS41My0zLjA4NGEuNzUuNzUgMCAwIDEgLjIxNi0uNjY0bDIuMjQtMi4xODMtMy4wOTYtLjQ1QS43NS43NSAwIDAgMSA5LjM4NSA1LjVMOCAyLjY5NFoiPjwvcGF0aD48L3N2Zz4=" /></a>
<a href="https://github.com/13335637282/Chatting/issues"><img alt="Issues" title="Issues" src="https://img.shields.io/github/issues/13335637282/Chatting?label=Issues&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggOS41YTEuNSAxLjUgMCAxIDAgMC0zIDEuNSAxLjUgMCAwIDAgMCAzWk04IDBBOCA4IDAgMSAxIDAgOEE4IDggMCAwIDEgOCAwWk0xLjUgOEE2LjUgNi41IDAgMSAwIDEzIDggNi41IDYuNSAwIDAgMCAxLjUgOFoiPjwvcGF0aD48L3N2Zz4=" /></a>
<a href="https://github.com/13335637282/Chatting/pulls"><img alt="Pull Requests" title="Pull Requests" src="https://img.shields.io/github/issues-pr/13335637282/Chatting?label=Pull%20Requests&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTEuNSAzLjI1YTIuMjUgMi4yNSAwIDEgMSAzIDIuMTIydjUuMjU2YTIuMjUxIDIuMjUxIDAgMSAxLTEuNSAwVjUuMzcyQTIuMjUgMi4yNSAwIDAgMSAxLjUgMy4yNVptNS42NzctLjE3N0w5LjU3My42NzdBLjI1LjI1IDAgMCAxIDEwIC44NTRWMi41aDFBMi41IDIuNSAwIDAgMSAxMy41IDV2NS42MjhhMi4yNTEgMi4yNTEgMCAxIDEtMS41IDBWNWExIDEgMCAwIDAtMS0xaC0xdjEuNjQ2YS4yNS4yNSAwIDAgMS0uNDI3LjE3N0w3LjE3NyAzLjQyN2EuMjUuMjUgMCAwIDEgMC0uMzU0Wk0zLjc1IDIuNWEuNzUuNzUgMCAxIDAgMCAxLjUuNzUuNzUgMCAwIDAgMC0xLjVabTAgOS41YS43NS43NSAwIDEgMCAwIDEuNS43NS43NSAwIDAgMCAwLTEuNVptOC4yNSAuNzVhLjc1Ljc1IDAgMSAwIDEuMCAwIC43NS43NSAwIDAgMC0xLjUgMFoiPjwvcGF0aD48L3N2Zz4=" /></a>
<a href="https://github.com/13335637282/Chatting/discussions"><img alt="Discussions" title="Discussions" src="https://img.shields.io/github/discussions/13335637282/Chatting?label=Discussions&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTEuNzUgMWg4LjVjLjk2NiAwIDEuNzUuNzg0IDEuNzUgMS43NXY1LjVBMS43NSAxLjc1IDAgMCAxIDEwLjI1IDEwSDcuMDYxbC0yLjU3NCAyLjU3M0ExLjQ1OCAxLjQ1OCAwIDAgMSAyIDExLjU0M1YxMEgtLjI1QTEuNzUgMS43NSAwIDAgMSAwIDguMjV2LTUuNUMwIDEuNzg0Ljc4NCAxIDEuNzUgMVpNMS41IDIuNzV2NS41YzAgLjEzOC4xMTIuMjUuMjUuMjVoMWEuNzUuNzUgMCAwIDEgLjc1Ljc1djIuMTlsMi43Mi0yLjcyYS43NDkuNzQ5IDAgMCAxIC41My0uMjJoMy41YS4yNS4yNSAwIDAgMCAuMjUtLjI1di01LjVhLjI1LjI1IDAgMCAwLS4yNS0uMjVoLTguNWEuMjUuMjUgMCAwIDAtLjI1LjI1Wm0xMyAyYS4yNS4yNSAwIDAgMC0uMjUtLjI1aC0uNWEuNzUuNzUgMCAwIDEgMC0xLjVoLjVjLjk2NiAwIDEuNzUuNzg0IDEuNzUgMS43NXY1LjVBMS43NSAxLj35IDAgMCAxIDE0LjI1IDEySDE0djEuNTQzYTEuNDU4IDEuNDU4IDAgMCAxLTIuNDg3IDEuMDNMOS4yMiAxMi4yOGEuNzQ5Ljc0OSAwIDAgMSAuMzI2LTEuMjc1QS43NDkuNzQ5IDAgMCAxIDEwIDExLjVhLjc0OS43NDkgMCAwIDEgLjczNC4yMTVsMi4yMiAyLjIydi0yLjE5YS43NS43NSAwIDAgMSAuNzUtLjc1aDFhLjI1LjI1IDAgMCAwIC4yNS0uMjVaIj48L3BhdGg+PC9zdmc+" /></a>
</p>

Chatting 是一个基于 PySide6 开发的轻量级开源聊天客户端，搭配 Flask 后端实现用户认证与 Token 管理。
客户端密码在传输前使用 RSA 公钥加密，服务端采用 Argon2 算法进行密码哈希存储，以提升基础安全能力。

## 开源协议
本项目基于 **Apache License 2.0** 开源，使用前请仔细阅读并遵守协议条款。

## 其他文档

| 文档 | 链接 |
| :----: | :----: |
| 开发文档 | [DEVELOPMENT.md](DEVELOPMENT.md) |
| 致谢名单 | [CREDITS.md](CREDITS.md) |
| 贡献指南 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 主 README | [README.md](README.md) |

## ✨ 功能特性

### 已完成
- [x] 用户注册 / 登录
- [x] 服务端 Token 生成与管理
- [x] 好友系统（发送请求、接受/拒绝、好友列表）

### 规划中
- [ ] 单聊 / 群聊消息功能
- [ ] 消息撤回、引用、回复
- [ ] 文件传输、表情包
- [ ] 语音 / 视频通话
- [ ] 群组管理
- [ ] 完善接口权限体系

## 📦 安装与部署

### 环境要求
- Python 3.10 ~ 3.11
- pip

### 部署流程
1. 克隆本仓库
2. 安装项目依赖
3. 进入 `server` 目录，运行 `server.py`
4. 等待 `PRIVATE_KEY.chatting` 和 `PUBLIC_KEY.chatting` 自动生成
5. 将 `PUBLIC_KEY.chatting` 复制到 `client` 目录
6. 运行 `client/client_ui.py`，注册测试账号
7. 进入主界面 → 设置 → 网络，配置服务器地址
8. 关闭服务端与客户端
9. 清理 `server` 目录中除 `server.py`、`PRIVATE_KEY.chatting`、`PUBLIC_KEY.chatting` 以外的临时文件
10. 重新启动服务端
11. 可选：删除 `client/client.log`
12. 打包 `client` 目录分发给用户使用

> 重要提示：
> 本项目为**学习与演示用途**，未经过大规模安全审计与高并发压力测试。
> 如用于公网生产环境，需自行完成安全加固、渗透测试、日志审计、数据备份等工作。

---

# 📝 法律声明与免责条款

## 1. 合规部署要求
- 任何个人或组织将本软件部署于**公网环境**对外提供服务时，必须**自行遵守所在国家/地区法律法规**，完成必要的备案、许可、安全评估与合规审批。
- 使用者应自行确保服务符合网络安全、数据安全、个人信息保护、电信业务管理等相关监管要求。

## 2. 使用限制
- 本软件**不得用于任何违法、违规、侵权或危害他人安全的活动**，包括但不限于：
  - 网络攻击、入侵、数据窃取、恶意传播
  - 诈骗、骚扰、非法监控、侵犯隐私
  - 传播违法信息、垃圾信息、恶意程序
  - 其他违反法律法规、公序良俗或侵害第三方合法权益的行为

## 3. 知识产权与开源协议
- 本项目基于 **Apache License 2.0** 开源授权。
- 你可以自由使用、修改、分发本软件，但必须保留原版权声明与许可协议。
- 未经授权不得将项目名称、作者信息用于虚假宣传、商业背书或误导性宣传。

## 4. 责任声明
- 本项目为**开源免费软件**，仅用于**学习、研究与技术交流**。
- 作者及所有贡献者**不为任何使用者的部署行为、运营行为、二次开发行为承担法律责任**。
- 因使用、修改、分发本软件而导致的任何直接或间接损失（包括但不限于数据泄露、服务中断、经济损失、法律纠纷等），均由**使用者自行承担全部责任**。
- 如使用者利用本软件从事违法犯罪活动，一切法律后果由使用者独立承担，作者及贡献者不承担任何连带责任。

## 5. 无担保声明
- 本软件按“**现状**”提供，**不附带任何明示或默示的担保**，包括但不限于：
  - 不保证适用于特定用途
  - 不保证无错误、无漏洞、无中断
  - 不保证安全性、可靠性、稳定性
- 作者不承诺提供持续维护、技术支持或漏洞修复。

## 6. 隐私与数据安全提示
- 本项目仅实现基础加密传输与密码存储，**未达到金融级、政务级安全标准**。
- 使用者自行负责用户数据、聊天记录、个人信息的安全保护、存储与备份。
- 如涉及敏感信息或个人数据，应自行补充加密、审计、访问控制等安全措施。

## 7. 条款适用
- 任何人下载、安装、运行、修改或分发本软件，即视为**已阅读、理解并完全同意本声明全部条款**。
- 如不同意本条款，应立即停止使用并删除所有相关文件。
