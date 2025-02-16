# Telegram Bot

这是一个使用 Python 创建的 Telegram 机器人项目。该项目使用 `python-telegram-bot` 库来实现与 Telegram API 的交互。

## 项目结构

```
telegram-bot
├── src
│   ├── bot.py          # Telegram 机器人的主程序
│   └── config.py       # 配置设置，包括访问令牌
├── requirements.txt     # 项目所需的 Python 库
└── README.md            # 项目的文档
```

## 安装依赖项

在开始之前，请确保您已安装 Python 3.x。然后，您可以使用以下命令安装项目所需的依赖项：

```bash
pip install -r requirements.txt
```

## 启动机器人

1. 在 `src/config.py` 文件中，确保您已正确设置 `TOKEN` 常量为您的 Telegram 机器人访问令牌。
2. 运行 `src/bot.py` 文件以启动机器人：

```bash
python src/bot.py
```

## 使用说明

启动机器人后，您可以通过 Telegram 与其聊天。机器人将响应您发送的消息。