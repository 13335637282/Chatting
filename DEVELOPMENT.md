# Chatting 开发文档

## 调用 客户端 api
[待完善，目前接口不是很多所以翻翻 client_api.py 勉强够用]

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

### 获取用户详细信息 `GET /users/<username>?token=<token>`
**路径参数**：`username` - 要查询的用户名  
**查询参数**：`token` - 当前登录用户的token  

**响应（自己或好友）**
- `200 OK`：返回用户详细信息
  ```json
  {
    "username": "alice",
    "created_at": "2024-01-01 12:00:00",
    "nickname": "爱丽丝",
    "birthday": "1995-05-20",
    "gender": "female",
    "avatar": "base64_encoded_image_data",
    "email": "alice@example.com",
    "phone": "13800138000",
    "bio": "Hello, I'm Alice!",
    "updated_at": "2024-01-02 10:30:00"
  }
  ```

**响应（非好友）**
- `403 Forbidden`：只有好友才能查看详细信息
  ```json
  { "error": "只有好友才能查看详细信息" }
  ```

**状态码**
- `200 OK`：成功
- `400 Bad Request`：缺少token参数[返回体中有error对象]
- `401 Unauthorized`：token无效或已过期[返回体中有error对象]
- `403 Forbidden`：无权限查看（非好友）[返回体中有error对象]
- `404 Not Found`：用户不存在[返回体中有error对象]

### 更新用户资料 `PUT /users/<username>/profile`
**路径参数**：`username` - 要更新资料的用户名  

**请求体**（所有字段均为可选）
```json
{
  "token": "user_token_here",
  "nickname": "新昵称",
  "birthday": "1995-05-20",
  "gender": "male",
  "avatar": "base64_encoded_image_data",
  "email": "newemail@example.com",
  "phone": "13800138000",
  "bio": "个人简介"
}
```

**响应**
- `200 OK`：资料更新成功
  ```json
  { "message": "资料更新成功" }
  ```

**状态码**
- `200 OK`：成功
- `400 Bad Request`：请求体不是JSON或没有提供更新字段[返回体中有error对象]
- `401 Unauthorized`：token无效或已过期[返回体中有error对象]
- `403 Forbidden`：只能更新自己的资料[返回体中有error对象]

### 修改用户名 `PUT /users/<old_username>/rename`
**路径参数**：`old_username` - 当前用户名  

**请求体**
```json
{
  "token": "user_token_here",
  "new_username": "new_username123"
}
```

**响应**
- `200 OK`：用户名修改成功
  ```json
  {
    "message": "用户名修改成功",
    "new_username": "new_username123"
  }
  ```

**状态码**
- `200 OK`：成功
- `400 Bad Request`：缺少token或新用户名，或用户名长度小于3[返回体中有error对象]
- `401 Unauthorized`：token无效或已过期[返回体中有error对象]
- `403 Forbidden`：只能修改自己的用户名[返回体中有error对象]
- `409 Conflict`：新用户名已存在[返回体中有error对象]
- `500 Internal Server Error`：服务器内部错误[返回体中有error对象]

### 搜索用户 `GET /users/search?q=<query>&token=<token>`
**查询参数**
- `q`：搜索关键词（至少2个字符）
- `token`：当前登录用户的token

**响应**
- `200 OK`：返回匹配的用户名列表
  ```json
  {
    "users": [
      "alice123",
      "alice_smith",
      "alice_wonder"
    ]
  }
  ```

**状态码**
- `200 OK`：成功
- `400 Bad Request`：缺少token参数或搜索词长度小于2[返回体中有error对象]
- `401 Unauthorized`：token无效或已过期[返回体中有error对象]

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
        "username": "bob",
        "nickname": "鲍勃",
        "created_at": "2024-01-01 12:00:00"
      }
    ]
  }
  ```
- `401 Unauthorized`：token无效[返回体中有error对象]

#### 删除好友 `DELETE /friends/<friend_username>`
**路径参数**：`friend_username` - 好友的用户名  
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

## 注意
一般建议直接调用 client_api.py 中的接口，接口用途详见doc string

## 🐛 故障排查

| 现象                               | 可能原因                         | 解决方法                                |
|----------------------------------|------------------------------|-------------------------------------|
| 客户端启动提示缺少公钥文件                    | `PUBLIC_KEY.chatting` 未复制到目录 | 从服务端复制公钥文件至客户端运行目录                  |
| 注册/登录时提示“服务器无法理解请求”              | RSA 解密失败，公钥与服务端不匹配           | 确认客户端使用的公钥与服务器私钥配对                  |
| 服务端启动时报错“Address already in use” | 端口 5000 已被占用                 | 修改 `server.py` 中的 `port` 参数，或关闭占用程序 |
| 客户端连接超时                          | 服务端未启动或网络不通                  | 检查服务端运行状态及防火墙设置                     |
| 发送好友请求时提示“用户不存在”                 | 输入的用户名错误                     | 确认好友用户名是否正确                        |
| 无法接受好友请求                         | token无效或请求已被处理               | 重新登录或检查请求状态                        |

## 🗄 数据库结构 [暂未更新，可能有误]

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

### user_profile.db（新增）
**user_profiles表**
- `username` TEXT PRIMARY KEY
- `nickname` TEXT
- `birthday` TEXT
- `gender` TEXT
- `avatar` TEXT
- `email` TEXT
- `phone` TEXT
- `bio` TEXT
- `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE

|           文档            |
|:-----------------------:|
| [开发文档](DEVELOPMENT.md)  |
|   [致谢名单](CREDITS.md)    |
| [贡献指南](CONTRIBUTING.md) |
|   [README](README.md)   |