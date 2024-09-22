from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, CommandHandler, MessageHandler, InlineQueryHandler, filters
from configparser import ConfigParser

# Читання токену з конфігураційного файлу
cfg = ConfigParser()
cfg.read('config.ini')
token = cfg['token']['key']

# Створення екземпляру Application
application = Application.builder().token(token).build()

# Функція для команди /start
async def start(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

# Функція для повторення тексту, який відправив користувач
async def echo(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
application.add_handler(echo_handler)

# Функція для команди /caps
async def caps(update: Update, context):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
application.add_handler(caps_handler)

# Функція для inline режиму
async def inline_caps(update: Update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

inline_caps_handler = InlineQueryHandler(inline_caps)
application.add_handler(inline_caps_handler)

# Функція для невідомих команд
async def unknown(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(filters.COMMAND, unknown)
application.add_handler(unknown_handler)

# Запуск бота
if __name__ == '__main__':
    application.run_polling()