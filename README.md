# happynet
跨平台(Windows, Linux, MacOS)的happyn客户端

# 打包命令
```
pyinstaller -F -w -i happynet.ico --add-data "happynet.ico;." --add-data "platforms;platforms" main.py
```