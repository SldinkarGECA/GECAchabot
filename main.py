import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    message = "Welcome to GECA NOTICE BOARD.\nThis bot is in development and new features will be added soon."
    update.message.reply_text(message)


def help(update, context):
    message = "Welcome to GECA NOTICE BOARD.\nUse /start to start.\n" \
              "Use /help to know about all the commands.\nUse /today to see today's notices.\n" \
              "On any other commands all the notices will be displayed.\nEnjoy!!"
    update.message.reply_text(message)


def all(update, context):
    url = "http://geca.ac.in/geca-downloads.aspx"
    try:
        page = urlopen(url)
    except:
        print("Error opening the URL")
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('table', {"class": "table table-striped table-bordered"})
    table_body = content.find('tbody')
    rows = table_body.find_all('tr')
    dates = []
    messages=[]
    for i in rows:
        cols = i.find_all('td')
        dates.append(cols[0].text.strip())
        link = "http://geca.ac.in/" + cols[1].find('a').get('href')
        link = link.replace(" ", "%20")
        extralink = cols[1].get('href')
        message = cols[0].text.strip() + "-->" + cols[1].text.strip() + "\n" + link
        if extralink is not None:
            message = message + "\n" + extralink
        messages.append(message)
        # update.message.reply_text(message)
    messages.reverse()
    for i in messages:
        update.message.reply_text(i)

def today(update, context):
    url = "http://geca.ac.in/geca-downloads.aspx"
    try:
        page = urlopen(url)
    except:
        print("Error opening the URL")
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.find('table', {"class": "table table-striped table-bordered"})
    table_body = content.find('tbody')
    rows = table_body.find_all('tr')
    dates = []
    messages = []
    for i in rows:
        cols = i.find_all('td')
        dates.append(cols[0].text.strip())
        link = "http://geca.ac.in/" + cols[1].find('a').get('href')
        link = link.replace(" ", "%20")
        format_str = '%m/%d/%Y'
        date = datetime.datetime.strptime(cols[0].text.strip(), format_str)
        tod = datetime.date.today()
        tod = datetime.datetime.strptime(str(tod), '%Y-%m-%d')
        message = cols[0].text.strip() + "-->" + cols[1].text.strip() + "\n" + link
        # update.message.reply_text(message)
        if date == tod:
            messages.append(message)
    if len(messages) == 0:
        update.message.reply_text("NO NOTICE TODAY")
    else:
        for i in messages:
            update.message.reply_text(i)


def echo(update, context):
    update.message.reply_text("USE PROPER COMMANDS")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("bot_token", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("today", today))
    dp.add_handler(CommandHandler("all", all))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
