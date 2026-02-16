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
