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
## 📖 API 文档

所有 API 端点前缀为 `/api/<版本号>`。请求与响应均为 JSON 格式。

如需向用户展示错误，建议返回请求体里的error对象 (如果有的话)，  
下列有error 对象的返回值，会在末尾标注 [返回体中有error对象]

在client中 login 等 函数的状态码返回-1则为和服务器发送/接受请求的时候发生错误，需特殊处理

### 用户注册 `POST /users`
**请求体**
```json
{
  "username": "alice",
  "password": "<Base64 编码的 RSA 加密密码>"
}
```
**响应**
- `201 Created`：注册成功
  ```json
  { "message": "用户创建成功" }
  ```
- `400 Bad Request`：请求格式错误或字段缺失[返回体中有error对象]
- `409 Conflict`：用户名已存在[返回体中有error对象]

### 用户登录 `POST /sessions`
**请求体**  
（同注册）  
**响应**
- `200 OK`：登录成功，返回 Token
  ```json
  {
    "message": "登录成功",
    "username": "<用户名>",
    "token": "uuid-token"
  }
  ```
- `401 Unauthorized`：用户名或密码错误[返回体中有error对象]
- `400 Bad Request`：请求格式错误[返回体中有error对象]

### 获取用户信息 `GET /users/<token>`
*警告: 此向请求还在开发阶段，未来有计划移除这项接口*  

**路径参数**：`token` - 登录时获得的 Token  
**响应**
- `200 OK`：返回用户基本信息
  ```json
  {
    "id": <id>,
    "username": "<用户名>"
  }
  ```
- `401 Unauthorized`：Token 无效或过期[返回体中有error对象]
- `404 Not Found`：用户不存在[返回体中有error对象]

### 登出 `DELETE /sessions`
**请求体**
```json
{ "token": "token" }
```
**响应**
- `200 OK`：登出成功 [返回体中有msg对象]
- `401 Unauthorized`：Token 无效 [返回体中有error对象]

### 好友系统 API

#### 发送好友请求 `POST /friends/requests`
**请求体**
```json
{
  "token": "用户token",
  "friend_username": "好友用户名",
  "message": "附加消息（可选）"
}
```
**响应**
- `201 Created`：好友请求已发送
  ```json
  { "message": "好友请求已发送" }
  ```
- `200 OK`：重新发送被拒绝的好友请求
  ```json
  { "message": "好友请求已重新发送" }
  ```
- `400 Bad Request`：参数错误或不能添加自己为好友[返回体中有error对象]
- `401 Unauthorized`：token无效[返回体中有error对象]
- `404 Not Found`：好友用户不存在[返回体中有error对象]
- `409 Conflict`：已经是好友关系或已存在待处理的请求[返回体中有error对象]

#### 获取收到的好友请求 `GET /friends/requests/incoming?token=<token>`
**查询参数**：`token` - 用户token  
**响应**
- `200 OK`：返回收到的待处理好友请求列表
  ```json
  {
    "requests": [
      {
        "request_id": 1,
        "from_user_id": 2,
        "from_username": "bob",
        "message": "加个好友吧",
        "created_at": "2024-01-01 12:00:00"
      }
    ]
  }
  ```
- `401 Unauthorized`：token无效[返回体中有error对象]

#### 获取发出的好友请求 `GET /friends/requests/outgoing?token=<token>`
**查询参数**：`token` - 用户token  
**响应**
- `200 OK`：返回发出的好友请求列表（包含所有状态）
  ```json
  {
    "requests": [
      {
        "request_id": 1,
        "to_user_id": 2,
        "to_username": "bob",
        "message": "加个好友吧",
        "status": "pending",  // pending, accepted, rejected
        "created_at": "2024-01-01 12:00:00"
      }
    ]
  }
  ```
- `401 Unauthorized`：token无效[返回体中有error对象]

#### 接受好友请求 `POST /friends/requests/<request_id>/accept`
**路径参数**：`request_id` - 好友请求ID  
**请求体**
```json
{
  "token": "用户token"
}
```
**响应**
- `200 OK`：已接受好友请求
  ```json
  { "message": "已接受好友请求" }
  ```
- `401 Unauthorized`：token无效[返回体中有error对象]
- `403 Forbidden`：无权操作此请求[返回体中有error对象]
- `404 Not Found`：请求不存在或已被处理[返回体中有error对象]

#### 拒绝好友请求 `POST /friends/requests/<request_id>/reject`
**路径参数**：`request_id` - 好友请求ID  
**请求体**
```json
{
  "token": "用户token"
}
```
**响应**
- `200 OK`：已拒绝好友请求
  ```json
  { "message": "已拒绝好友请求" }
  ```
- `401 Unauthorized`：token无效[返回体中有error对象]
- `403 Forbidden`：无权操作此请求[返回体中有error对象]
- `404 Not Found`：请求不存在或已被处理[返回体中有error对象]

#### 获取好友列表 `GET /friends?token=<token>`
**查询参数**：`token` - 用户token  
**响应**
- `200 OK`：返回好友列表
  ```json
  {
    "friends": [
      {
        "user_id": 2,
        "username": "bob",
        "created_at": "2024-01-01 12:00:00"
      }
    ]
  }
  ```
- `401 Unauthorized`：token无效[返回体中有error对象]

#### 删除好友 `DELETE /friends/<friend_id>`
**路径参数**：`friend_id` - 好友的用户ID  
**请求体**
```json
{
  "token": "用户token"
}
```
**响应**
- `200 OK`：好友已删除
  ```json
  { "message": "好友已删除" }
  ```
- `401 Unauthorized`：token无效[返回体中有error对象]

### 健康检查 `GET /health`
**响应**
```json
{ "error": "ok" }
```
*注意：健康检查返回的字段名为"error"但实际表示服务正常*

## 🐛 故障排查

| 现象                               | 可能原因                         | 解决方法                                |
|----------------------------------|------------------------------|-------------------------------------|
| 客户端启动提示缺少公钥文件                    | `PUBLIC_KEY.chatting` 未复制到目录 | 从服务端复制公钥文件至客户端运行目录                  |
| 注册/登录时提示“服务器无法理解请求”              | RSA 解密失败，公钥与服务端不匹配           | 确认客户端使用的公钥与服务器私钥配对                  |
| 服务端启动时报错“Address already in use” | 端口 5000 已被占用                 | 修改 `server.py` 中的 `port` 参数，或关闭占用程序 |
| 客户端连接超时                          | 服务端未启动或网络不通                  | 检查服务端运行状态及防火墙设置                     |
| 发送好友请求时提示“用户不存在”                 | 输入的用户名错误                     | 确认好友用户名是否正确                        |
| 无法接受好友请求                         | token无效或请求已被处理               | 重新登录或检查请求状态                        |

## 🗄 数据库结构

### login.db
**users表**
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `username` TEXT UNIQUE NOT NULL
- `password` TEXT NOT NULL (Argon2哈希值)

### friends.db
**friends表**
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `user_id` INTEGER NOT NULL
- `friend_id` INTEGER NOT NULL
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- UNIQUE(user_id, friend_id)

### friend_requests.db
**friend_requests表**
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `from_user_id` INTEGER NOT NULL
- `to_user_id` INTEGER NOT NULL
- `status` TEXT DEFAULT 'pending' (pending, accepted, rejected)
- `message` TEXT
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- UNIQUE(from_user_id, to_user_id)

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
