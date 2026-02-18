# Chatting 开发文档
## 客户端 API
建议不要手动使用下列接口。建议使用 client_api 中的函数来完成调用，如对此api函数定义不熟悉请参阅 [Python 客户端开发文档](#client-api-文档)。
### 📖 API 文档

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

## client api 文档



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