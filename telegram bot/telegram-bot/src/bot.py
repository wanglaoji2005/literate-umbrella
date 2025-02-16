import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask, request, jsonify # type: ignore
import threading
from config import TOKEN

try:
    from payment import check_payment_status # type: ignore
except ImportError:
    def check_payment_status():
        return "无法检查支付状态，模块未找到。"

# 启用日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask 应用
app = Flask(__name__)

# 模拟数据库
transactions = {}
exchange_rates = {
    "z0": [{"商家": f"商家{i}", "汇率": 6.5 + i * 0.1, "支付方式": "全部"} for i in range(10)],
    "lk": [{"商家": f"商家{i}", "汇率": 6.6 + i * 0.1, "支付方式": "银行卡"} for i in range(10)],
    "lz": [{"商家": f"商家{i}", "汇率": 6.7 + i * 0.1, "支付方式": "支付宝"} for i in range(10)],
    "lw": [{"商家": f"商家{i}", "汇率": 6.8 + i * 0.1, "支付方式": "微信"} for i in range(10)],
}

# AI 聊天功能
def ai_chat(text):
    response = f"AI: 你说了 '{text}'"
    return response

# 查账功能
def check_account(user_id):
    if user_id in transactions:
        return f"账户余额：{transactions[user_id]['balance']}元\n交易记录：{transactions[user_id]['history']}"
    else:
        return "账户不存在或没有交易记录。"

# 记账功能
def record_transaction(user_id, amount, description):
    if user_id not in transactions:
        transactions[user_id] = {"balance": 0, "history": []}
    transactions[user_id]["balance"] += amount
    transactions[user_id]["history"].append(f"{description}: {amount}元")
    return f"已记录：{description}，金额：{amount}元"

# Okex 商家实时交易汇率 Top10
def get_okex_top10(payment_method):
    return exchange_rates.get(payment_method, [])

# Telegram Bot 命令处理
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('你好！我是你的Telegram机器人。')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('发送 /start 开始聊天，发送 /check_payment 查询支付状态。')

def handle_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('你说的是：' + update.message.text)

def check_payment(update: Update, context: CallbackContext) -> None:
    status = check_payment_status()
    update.message.reply_text(f'支付状态：{status}')

def chat(update: Update, context: CallbackContext):
    user_text = update.message.text
    ai_response = ai_chat(user_text)
    update.message.reply_text(ai_response)

def check_account_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    account_info = check_account(user_id)
    update.message.reply_text(account_info)

def record_transaction_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    args = context.args
    if len(args) < 2:
        update.message.reply_text("用法：/record <金额> <描述>")
        return
    try:
        amount = float(args[0])
        description = ' '.join(args[1:])
        result = record_transaction(user_id, amount, description)
        update.message.reply_text(result)
    except ValueError:
        update.message.reply_text("金额必须是数字。")

def okex_top10(update: Update, context: CallbackContext):
    payment_method = context.args[0] if context.args else 'z0'
    top10 = get_okex_top10(payment_method)
    if top10:
        response = "\n".join([f"{item['商家']} - {item['汇率']} ({item['支付方式']})" for item in top10])
        update.message.reply_text(f"Top 10 汇率 ({payment_method}):\n{response}")
    else:
        update.message.reply_text("未找到相关支付方式的汇率数据。")

# 自动回复功能
def auto_reply(update: Update, context: CallbackContext):
    user_text = update.message.text
    update.message.reply_text(f"自动回复：已收到你的消息 '{user_text}'")

# 网页查单功能
@app.route('/check_order', methods=['POST'])
def check_order():
    data = request.json
    if data.get("api_key") != TOKEN:
        return jsonify({"status": "error", "message": "无效的 API 密钥"}), 401
    order_id = data.get("order_id")
    return jsonify({"status": "success", "order_id": order_id, "details": "订单详情"})

# 设置 Telegram Bot
def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("check_payment", check_payment))
    dispatcher.add_handler(CommandHandler("chat", chat))
    dispatcher.add_handler(CommandHandler("check_account", check_account_command))
    dispatcher.add_handler(CommandHandler("record", record_transaction_command))
    dispatcher.add_handler(CommandHandler("okex_top10", okex_top10))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_reply))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: app.run(port=5000))
    flask_thread.start()
    main()