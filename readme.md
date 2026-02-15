# Chatting 项目说明
## 基础说明
- 本项目基于 textual  TUI 框架开发  
- 本项目依赖库见下表  

| Server端     | Client端   |
|-------------|-----------|
| logging     | threading |
| sqlite3     | requests  |
| hashlib     | textual   |
| uuid        | rich      |
| flask       | rsa       |
| rsa         | inspect   |
| argon2-cffi | os        |
| base64      | re        |
|             | time      |
|             | typing    |
|             | base64    |

- 运行服务器端/客户端均只需通过 python 运行py文件即可
- 项目目标是提供一个便捷的聊天软件

## 项目待完善的功能
- 聊天功能
  + [ ] 私聊
  + [ ] 群聊
  + [ ] 撤回
  + [ ] 引用
  + [ ] 表情包
  + [ ] 收发文件
  + [ ] 语音通话
  + [ ] 共享屏幕
  + [x] 登录/注册
  + [x] token生成
  + [ ] 加好友
  + [ ] 加群
  + [ ] Chat ID
- 群功能
  + [ ] 群头衔
  + [ ] 禁言
  + [ ] 踢出
  + [ ] 邀请
  + [ ] 拉入黑名单
  + [ ] 进群审查
  + [ ] 解散
  + [ ] 创建
- [ ] 完善的api

## 如何安转
1. clone 此项目: `git clone https://github.com/13335637282/Chatting.git`
2. 将路径转移到 Chatting 文件夹下: `cd Chatting`
3. 运行安装依赖: `python -m pip install requirements.txt`
4. 运行 server.py 获得`PRIVATE_KEY.chatting` 和 `PUBLIC_KEY.chatting`文件
5. 将 `PUBLIC_KEY.chatting` 移动到 `client.py` 运行目录下 (如果你的 client 要分发给其他人的话 请不要将 `PRIVATE_KEY.chatting` 给其他人，以免造成密码泄露)
6. 修改 `client.py` 中的 BASE_URL 字段， 修改为你自己的服务器ip : `http://<your_server_ip>/api/v1`
7. 运行 `client.py` 测试是否可以正常使用 (如果不行请先确认是否是程序bug，如果是 请提交issue，如果无法确定请参阅故障排查)

## 故障排查
*因项目还在开放阶段，暂时没有。*

## 网络 API
*注: 以下省略最前面的/api/<api_version>*  
*当前 api_version 为 v1*  
  
### 注册
> POST /users  

返回状态码表格

| 状态码 | 含义                                                 |
|-----|----------------------------------------------------|
| 400 | 请求体不为json / 没有提供密码 和 用户名 /  rsa 解码错误 / 密码不是 str 类型 |
| 409 | 用户名已存在                                             |
| 201 | 创建成功                                               |

返回体:  
400 / 409 :
```
{
  "error": <str : 错误原因(人类可读)>
}
```

201 :
```
 {  
 "message": <str : 消息(人类可读)>  
}
```

### 登录
> POST /sessions  

| 状态码 | 含义                                         |
|-----|--------------------------------------------|
| 400 | 请求体不为json / 没有提供密码 和 用户名 / 在登录时发生了hash校验错误 |
| 200 | 登录成功将会返回一个 token                           |
| 401 | 用户名或密码错误                                   |

返回体:  
400 / 401 :
```
{
  "error": <error: str 错误原因(人类可读)>
}
```

200 :
```
{
  "message": "登录成功",
  "username": <username: str 用户名>,
  "token": <token: str 登录token>
}
```

## 协议
本项目协议主题存储在 LICENSE 文件夹， 为 Apache License 2.0 协议。以文件内容为准

## Bug 预警
所有操作均可能导致出现bug