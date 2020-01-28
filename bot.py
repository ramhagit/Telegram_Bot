import logging
import model
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, CallbackQueryHandler
import secrets


logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    name = update.effective_user['first_name'].split(" ")[0]
    # print(name)
    text = model.get_behind_name(name)
    msg = f"Hello {name} 🌹 \n\nYou have a wonderful name ✨\n\nHere is some info about it:\n\n{text}"
    context.bot.send_message(chat_id=chat_id, text=msg)
    keyboard = [[InlineKeyboardButton("Aries ♈", callback_data = '0'),
                InlineKeyboardButton("Taurus ♉", callback_data = '1'),
                InlineKeyboardButton("Gemini ♊", callback_data = '2')],
                [InlineKeyboardButton("Cancer ♋", callback_data = '3'),
                InlineKeyboardButton("Leo ♌", callback_data = '4'),
                InlineKeyboardButton("Virgo ♍", callback_data = '5')],
                [InlineKeyboardButton("Libra ♎", callback_data = '6'),
                InlineKeyboardButton("Scorpio ♏", callback_data = '7'),
                InlineKeyboardButton("Sagittarius ♐", callback_data = '8')],
                [InlineKeyboardButton("Capricorn ♑", callback_data = '9'),
                InlineKeyboardButton("Aquarius ♒", callback_data = '10'),
                InlineKeyboardButton("Pisces ♓", callback_data = '11')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # context.job_queue.run_once(reply_markup = InlineKeyboardMarkup(keyboard), when=1, context =chat_id)
    # context.job_queue.run_once(update.message.reply_text('Which Zodiac sign are you?', reply_markup = reply_markup), when=1, context =chat_id)
    update.message.reply_text('Which Zodiac sign are you?', reply_markup = reply_markup)


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    response = model.get_behind_name(text)
    context.bot.send_message(chat_id=update.message.chat_id, text=response)


def button(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    query = update.callback_query
    msg = f"💖❤💕  LOVE IS IN THE AIR... {chr(9800+int(query.data))}💋"
    query.edit_message_text(text = msg)
    bio = model.matches_plot(query.data)
    bio.seek(0)
    # context.job_queue.run_daily(callback_alarm, context = update.message.chat_id, days = (0, 1, 2, 3, 4, 5, 6), time = time(hour = 10, minute = 10, second = 10))
    context.bot.send_photo(chat_id = chat_id, photo = bio)
    text = "LET'S FIND YOUR LOVER!!!💖\n\nChoose your favorite path:\n\n /Tarot\n\n           /Stars\n\n                    /Numerology"
    context.bot.send_message(chat_id = chat_id, text = text)


def cards(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.effective_chat.id
    if text == '/Tarot':
        i = 0
        context.bot.send_photo(chat_id = chat_id, photo = open('tarot.jpg', 'rb'))
    if text == '/Stars':
        i = 1
        context.bot.send_photo(chat_id = chat_id, photo = open('star_maps.jpg', 'rb'))
    if text == '/Numerology':
        i = 2
        context.bot.send_photo(chat_id = chat_id, photo = open('numerology.jpg', 'rb'))
    # for i in range(6):
    #     context.bot.send_photo(chat_id=chat_id, photo=open('Tarot-Deck-main.jpg', 'rb'))


def main():
    updater = Updater(token=secrets.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, respond))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('Tarot', cards))
    dispatcher.add_handler(CommandHandler('Stars', cards))
    dispatcher.add_handler(CommandHandler('Numerology', cards))

    logger.info("* Start polling...")
    updater.start_polling()  # Starts polling in a background thread.
    updater.idle()  # Wait until Ctrl+C is pressed
    logger.info("* Bye!")


if __name__ == '__main__':
    main()
