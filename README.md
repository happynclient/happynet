# happynet
跨平台(Windows, Linux, MacOS)的happyn客户端V2版本，正在开发中；

Roadmap:

* 支持多平台
* 简单易用的UI
* 支持服务模式
* 支持用户自定义配置
* 支持多个场景切换
* 集成串流服务

# 打包命令
```
pyinstaller -F -w -i happynet.ico --add-data "happynet.ico;." --add-data "platforms;platforms" main.py
```
