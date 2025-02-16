# Code Citations

## License: 未知
https://github.com/wanglaoji2005/literate-umbrella.git

```
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler
```

{
  "configurations": [
    {
      "type": "debugpy",
      "request": "launch",
      "name": "Launch bot.py",
      "program": "${workspaceFolder}/${input:programPath}"
    }
  ],
  "inputs": [
    {
      "type": "pickString",
      "id": "programPath",
      "description": "Select the bot.py file to launch",
      "options": [
        "bot.py",
        "telegram-bot/src/bot.py"
      ]
    }
  ]
}

