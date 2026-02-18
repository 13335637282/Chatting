from typing import List

import maliang
import rich.traceback

rich.traceback.install()

from client_api import *

logged_in = False
token = ""
input_pwd_count = 0
pwds: List[str] = []

root = maliang.Tk(title="登录")
root.center()

cv = maliang.Canvas(auto_zoom=True, keep_ratio="min", free_anchor=True)
cv.place(width=1280, height=720, x=640, y=360, anchor="center")

maliang.Text(cv, (640, 200), text="账 号 登 录", fontsize=48, anchor="center")

maliang.Text(cv, (450, 300), text="账号", anchor="nw")
user_name = maliang.InputBox(cv, (450, 340), (380, 50), placeholder="点击输入账号")
maliang.Text(cv, (450, 400), text="密码", anchor="nw")
password = maliang.InputBox(
    cv, (450, 440), (380, 50), show="*", placeholder="点击输入密码"
)


def login_action():
    r = login(user_name.get(), password.get())
    if r.status_code == 200:
        maliang.TkMessage("登录成功!")
        global token

        global logged_in
        logged_in = True
        root.destroy()
        token = r.json().get("token")
    elif r.status_code != 200 and r.status_code != -1:
        maliang.TkMessage(f"登录失败: {r.json().get('error')}")
    else:
        maliang.TkMessage("发生了未知错误!")


def register_action():
    global input_pwd_count
    print(input_pwd_count, pwds, pwds.count(password.get()))
    pwds.append(password.get())
    if input_pwd_count >= 1 and pwds.count(password.get()) == 2:
        r = register(user_name.get(), password.get())
        if r.status_code == 201:
            maliang.TkMessage("注册成功!")
        elif r.status_code != 201 and r.status_code != -1:
            maliang.TkMessage(f"注册失败: {r.json().get('error')}")
        else:
            maliang.TkMessage("发生了未知错误!")
        password.clear()
        input_pwd_count = 0
    elif input_pwd_count < 1:
        maliang.TkMessage("请再输入一遍密码")
        password.clear()
        input_pwd_count += 1
    elif input_pwd_count >= 1 and pwds.count(password.get()) == 1:
        maliang.TkMessage("第二次输入与第一次不匹配! 请重新输入密码2次")
        input_pwd_count = 0
        password.clear()
        pwds.clear()


maliang.Button(
    cv, (450, 540), (180, 50), text="注 册", command=lambda: register_action()
)
maliang.Button(cv, (650, 540), (180, 50), text="登 录", command=lambda: login_action())

root.mainloop()
del root
if logged_in:
    root = maliang.Tk()
    root.mainloop()
