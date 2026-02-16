
# Chatting - 一个开源的聊天软件

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Chatting 是一个基于 Textual TUI 框架开发的轻量级聊天客户端，配合 Flask 后端实现用户认证与 Token 管理。所有密码在传输前均使用 RSA 公钥加密，服务端使用 Argon2 进行哈希存储，保障基础安全。

## ✨ 功能特性

### 已完成
- [x] 用户注册 / 登录
- [x] 服务端 Token 生成与维护
- [x] 命令行图形界面（TUI）

### 待完善
- [ ] 私聊 / 群聊
- [ ] 消息撤回与引用
- [ ] 文件传输与表情包
- [ ] 语音 / 视频通话
- [ ] 好友
- [ ] 群组管理
- [ ] 完善的 API 及权限控制

## 🛠 技术栈

| 组件     | 技术                                                                 |
|----------|----------------------------------------------------------------------|
| 客户端   | Python, Textual, Rich, Requests, RSA, Argon2                        |
| 服务端   | Python, Flask, SQLite, RSA, Argon2, logging, uuid                   |
| 加密     | RSA (密钥交换), Argon2 (密码哈希), Base64 (编码)                    |

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
   首次运行会在当前目录生成 `PRIVATE_KEY.chatting` 和 `PUBLIC_KEY.chatting`。  
   **注意**：`PRIVATE_KEY.chatting` 必须严格保密，仅保留在服务端。

4. 配置客户端
   - 将服务端生成的 `PUBLIC_KEY.chatting` 复制到客户端运行目录。
   - 修改 `client.py` 中的 `BASE_URL` 变量，指向你的服务端地址（格式 `http://your-server-ip:5000/api/v1` ）。

5. 运行客户端
   ```bash
   python client.py
   ```

## 📖 API 文档

所有 API 端点前缀为 `/api/v1`。请求与响应均为 JSON 格式。

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

### 健康检查 `GET /health`
**响应**
```json
{ "status": "ok" }
```

## 🐛 故障排查

| 现象                               | 可能原因                         | 解决方法                                |
|----------------------------------|------------------------------|-------------------------------------|
| 客户端启动提示缺少公钥文件                    | `PUBLIC_KEY.chatting` 未复制到目录 | 从服务端复制公钥文件至客户端运行目录                  |
| 注册/登录时提示“服务器无法理解请求”              | RSA 解密失败，公钥与服务端不匹配           | 确认客户端使用的公钥与服务器私钥配对                  |
| 服务端启动时报错“Address already in use” | 端口 5000 已被占用                 | 修改 `server.py` 中的 `port` 参数，或关闭占用程序 |
| 客户端连接超时                          | 服务端未启动或网络不通                  | 检查服务端运行状态及防火墙设置                     |

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request。在贡献代码前，请确保：
- 代码风格与现有代码保持一致。 
- 新功能包含必要的注释和文档。
- 提交前运行测试，确保原有功能正常。
### 格式化代码教程:
- cd 到你的工作目录
```bash
cd Chatting
```
- 安装 isort, black 工具
```bash
pip install isort
```
```bash
pip install black
```

- 格式化整个目录的文件
```bash
isort .
```
```bash
black .
```



以下是Windows演示
```
D:\> cd Chatting

D:\Chatting> pip install black
Collecting black
  Downloading black-26.1.0-cp313-cp313-win_amd64.whl.metadata (88 kB)
Requirement already satisfied: click>=8.0.0 in .\.venv\Lib\site-packages (from black) (8.3.1)
Requirement already satisfied: mypy-extensions>=0.4.3 in .\.venv\Lib\site-packages (from black) (1.1.0)
Collecting packaging>=22.0 (from black)
  Downloading packaging-26.0-py3-none-any.whl.metadata (3.3 kB)
Requirement already satisfied: pathspec>=1.0.0 in .\.venv\Lib\site-packages (from black) (1.0.4)
Requirement already satisfied: platformdirs>=2 in .\.venv\Lib\site-packages (from black) (4.7.0)
Collecting pytokens>=0.3.0 (from black)
  Downloading pytokens-0.4.1-cp313-cp313-win_amd64.whl.metadata (3.9 kB)
Requirement already satisfied: colorama in .\.venv\Lib\site-packages (from click>=8.0.0->black) (0.4.6)
Downloading black-26.1.0-cp313-cp313-win_amd64.whl (1.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.4/1.4 MB 6.5 MB/s  0:00:00
Downloading packaging-26.0-py3-none-any.whl (74 kB)
Downloading pytokens-0.4.1-cp313-cp313-win_amd64.whl (103 kB)
Installing collected packages: pytokens, packaging, black
Successfully installed black-26.1.0 packaging-26.0 pytokens-0.4.1

D:\Chatting> pip install isort
Collecting isort
  Downloading isort-7.0.0-py3-none-any.whl.metadata (11 kB)
Downloading isort-7.0.0-py3-none-any.whl (94 kB)
Installing collected packages: isort
Successfully installed isort-7.0.0

D:\Chatting> black .
reformatted D:\Chatting\logger.py
reformatted D:\Chatting\server.py
reformatted D:\Chatting\client.py

All done! ✨ 🍰 ✨
3 files reformatted.

D:\Chatting> isort .
Fixing D:\Chatting\logger.py
Fixing D:\Chatting\server.py
Fixing D:\Chatting\test.py
Skipped 3 files
```

## 📄 许可证

本项目基于 [Apache License 2.0](LICENSE) 开源。  
使用本项目时，请保留原始版权声明及许可证文本。