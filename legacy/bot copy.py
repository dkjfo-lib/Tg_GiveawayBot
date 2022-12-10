import os
import os.path
from pyclbr import Function
import sys
from uuid import UUID, uuid4
import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.ext import CallbackQueryHandler
from telegram.parsemode import ParseMode
import logging
from command import Command
from giveaway import Giveaway
from messageChecker import MessageChecker
from userInfo import UserInfo
import pickle
from chatFunc import ChatFunc

local = False
PORT = os.getenv('PORT', default=8443)
TOKEN = "5726668567:AAEnt_hRMirItfq2Jrn-srH8OGRz_oVjNOI"
HEROKU_APP = "chat-bot-yuki"

SUBSCRIBE_KEYWORD = 'subscribe_'
UNSUBSCRIBE_KEYWORD = 'unsubscribe_'
INFO_KEYWORD = 'info'
CURRENCY = 'Social Credit'
GIVEAWAYS_PATH = './giveaways'

WEBHOOK_URL = "https://{0}.herokuapp.com/{1}".format(HEROKU_APP, TOKEN) 

chatRules = [
    MessageChecker(['дефка', 'девка', 'месяки'], -500, CURRENCY, 'Отправляйся в гулаг грязный женаненавистник!'),
    MessageChecker(['gay', 'g@y', 'гей', '🏳️‍🌈', '👬'], -10, CURRENCY, ''),
    MessageChecker(['🇭🇰'], -100, CURRENCY, 'Петух обнаружен!'),
    MessageChecker(['🇨🇳'], 50, CURRENCY, 'Xi гордится тобой!')
]

# create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(fmt="[%(asctime)s] [%(levelname)-0.4s]\t%(message)s",
                              datefmt="%Y.%m.%d %H:%M:%S")

# add formatter to ch
ch.setFormatter(formatter)

# create file handler
fileHandler = logging.FileHandler("./log.log")
fileHandler.setFormatter(formatter)

# add console and file handlers to logger
logger.addHandler(ch)
logger.addHandler(fileHandler)

logger.info('logger created')


# "application" code
# logger.debug("debug message")
# logger.info("info message")
# logger.warning("warn message")
# logger.error("error message")
# logger.critical("critical message")



updater = Updater(TOKEN,
                  use_context=True)

bot = telegram.Bot(token=TOKEN)
chatFunc = ChatFunc(bot)



def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def loadGiveaway(giveawayId:str):
    with open(os.path.join(GIVEAWAYS_PATH, 'g_%s.pkl' % giveawayId), 'rb') as giveaway_file:
        giveaway :Giveaway = pickle.load(giveaway_file)
        return giveaway

def saveGiveaway(giveaway :Giveaway):
    if not os.path.exists(GIVEAWAYS_PATH):
        os.mkdir(GIVEAWAYS_PATH)
    with open(os.path.join(GIVEAWAYS_PATH, 'g_%s.pkl' % giveaway.id), 'wb') as giveaway_file:
        pickle.dump(giveaway, giveaway_file)

def checkIfAuthor(giveaway :Giveaway, update :Update, doStuff: Function):
    if update.effective_user.id == giveaway.author:
        doStuff(giveaway, update)
    else:
        chatFunc.sendDontHavePermission(update, giveaway)

def makeGiveawayPost(giveaway:Giveaway, update:Update):
    button_s = [telegram.InlineKeyboardButton(
        text='subscribe', callback_data=SUBSCRIBE_KEYWORD + str(giveaway.id))]
    button_u = [telegram.InlineKeyboardButton(
        text='unsubscribe', callback_data=UNSUBSCRIBE_KEYWORD + str(giveaway.id))]
    keyboard = telegram.InlineKeyboardMarkup([button_s, button_u])
    text = '<strong>{0}</strong>\n{1}'.format(giveaway.name, giveaway.description)
    if giveaway.photoId:
        bot.send_photo(
            chat_id = update.effective_chat.id,
            photo = giveaway.photoId,
            caption = text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )
    else:
        bot.send_message(
            chat_id = update.effective_chat.id,
            text = text,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )

def makeGiveawayEndPost(giveaway:Giveaway, update:Update, winners :str):
    text = '<strong>{0} has finished!</strong>\nCongratulations to our winners:\n{1}'.format(giveaway.name, winners )
    if giveaway.photoId:
        bot.send_photo(
            chat_id = update.effective_chat.id,
            photo = giveaway.photoId,
            caption = text,
            parse_mode=ParseMode.HTML,
        )
    else:
        bot.send_message(
            chat_id = update.effective_chat.id,
            text = text,
            parse_mode=ParseMode.HTML,
        )

def checkGiveawayId(update :Update,giveawayId :str):
    # check params are correct
    if not giveawayId:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='Please specify giveawayId')
        return False
    if not giveawayExists(giveawayId):
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='Giveaway with id "%s" does not exist' % giveawayId)
        return False
    return True

def giveawayExists(guid :str):
    return os.path.exists(os.path.join(GIVEAWAYS_PATH, 'g_%s.pkl' % guid))

# /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        """M'Lord, I am your trusty bot!""")

# /help
def help(update: Update, context: CallbackContext):
    update.message.reply_text("Go fuck yourself!")

# /html
def html(update: Update, context: CallbackContext):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello User, You have used <b>start</b> command. Search about developer on google, <a href='https://www.google.com/search?q=tbhaxor'>@tbhaxor</a>",
        parse_mode=ParseMode.HTML,
    )

# /info
def info(update: Update, context: CallbackContext):
    buttons = []
    buttons.append([telegram.InlineKeyboardButton(
        text='get info', callback_data=INFO_KEYWORD)])
    keyboard = telegram.InlineKeyboardMarkup(buttons)
    bot.sendMessage(chat_id=update.effective_chat.id,
                    text='get chat info', reply_markup=keyboard)

# /restart
def restart(update: Update, context: CallbackContext):
    bot.sendMessage(chat_id=update.effective_chat.id,
                    text='Bot will be back in 5 seconds!')
    chatFunc.deleteOriginalMessage(update) 
    restart_program()

# /reply
def reply(update: Update, context: CallbackContext):
    replyTo = update.message.text.replace('/reply', '').strip()
    bot.sendMessage(chat_id=update.effective_chat.id,
                    text='you said %s' % replyTo)

# /gc
def giveaway_createHandler(update: Update, cb: CallbackContext):
    logger.info('processing command "{0}"'.format(update.message.text))
    giveaway_create(update, update.effective_message.text)

# creates a new giveaway and a post about it
def giveaway_create(update :Update,command: str, photo_id :str = None):
    logger.info('processing command "{0}"'.format(command))
    giveawayInfo = command.replace('/g_create', '').strip().split("''")
    # check params are correct
    if len(giveawayInfo) != 3:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text="Expected three parameters in format \"/g_create Now''name''description\", but got %s parameters" % len(giveawayInfo))
        return
    if not giveawayInfo[1]:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='Giveaway is missing the name')
        return
    if not giveawayInfo[2]:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='Giveaway is missing the description')
        return
    if (not giveawayInfo[0]) | (not giveawayInfo[0].isdigit()):
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='Giveaway is missing the NumberOfWinners')
        return
    if int(giveawayInfo[0]) < 1:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='NumberOfWinners should be greater than zero')
        return


    newGiveaway = Giveaway(
        author = update.effective_user.id,
        authorNick = update.effective_user.name,
        name = giveawayInfo[1],
        description = giveawayInfo[2],
        NumberOfWinners = int(giveawayInfo[0]),
        id = uuid4(),
        subscribers = [],
        ended = False,
        winners = [],
        photoId = photo_id
    )
    saveGiveaway(newGiveaway)

    makeGiveawayPost(newGiveaway, update)
    bot.sendMessage(chat_id=newGiveaway.author,
                    text='New giveaway created!\ngiveawayId:{0}\nFirst posted in chatId:{1}\nNumberOfWinners:{2}\name:{3}\ndescription:{4}'.
                    format(newGiveaway.id, update.effective_chat.id,newGiveaway.numberOfWinners,newGiveaway.name,newGiveaway.description))
    chatFunc.deleteOriginalMessage(update) 

# /gp
def giveaway_post(update: Update, cb : CallbackContext):
    logger.info('processing command "{0}"'.format(update.message.text))
    giveawayId = update.message.text.replace('/g_post', '').strip()
    if not checkGiveawayId(update, giveawayId): 
        return
    giveaway = loadGiveaway(giveawayId)
    checkIfAuthor(giveaway, update, makeGiveawayPost)
    bot.sendMessage(chat_id= giveaway.author,
                    text='New giveaway post created!\ngiveawayId:{0}\nPosted in chatId:{1}'.
                    format(giveaway.id, update.effective_chat.id))
    chatFunc.deleteOriginalMessage(update) 

# /gs
def giveaway_subs(update: Update, cb : CallbackContext):
    logger.info('processing command "{0}"'.format(update.message.text))
    giveawayId = update.message.text.replace('/g_subs', '').strip()
    if not checkGiveawayId(update, giveawayId): 
        return
    giveaway = loadGiveaway(giveawayId)
    if update.effective_user.id == giveaway.author:
        subs = [sub.name for sub in giveaway.subscribers]
        subsDsc = "Number of subs: {0}\n{1}".format(str(len(subs)), '\n'.join(subs))
        bot.send_message(chat_id = update.effective_chat.id,
                        text = subsDsc)
    else:
        chatFunc.sendDontHavePermission(update, giveaway)
    chatFunc.deleteOriginalMessage(update) 

# /gf
def giveaway_finish(update :Update, cb :CallbackContext):
    logger.info('processing command "{0}"'.format(update.message.text))
    giveawayId = update.message.text.replace('/g_finish', '').strip()
    if not checkGiveawayId(update, giveawayId): 
        return
    giveaway = loadGiveaway(giveawayId)
    if update.effective_user.id == giveaway.author:
        winners = giveaway.getWinners()
        makeGiveawayEndPost(giveaway, update, winners)
        saveGiveaway(giveaway)
    else:
        chatFunc.sendDontHavePermission(update, giveaway)
    chatFunc.deleteOriginalMessage(update) 

# /ge
def giveaway_editHandler(update :Update, cb :CallbackContext):
    logger.info('processing command "{0}"'.format(update.message.text))
    giveaway_edit(update, update.effective_message.text)

def giveaway_edit(update :Update, command :str, photo_id :str = None):
    logger.info('processing command "{0}"'.format(command))
    giveawayInfo = command.replace('/g_edit', '').strip().split("''")
    # check params are correct
    if len(giveawayInfo) != 4:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text="Expected three parameters in format \"/g_edit GiveawayId''Now''name''description\", but got %s parameters" % len(giveawayInfo))
        return
    giveawayId = giveawayInfo[0]
    newNoW = giveawayInfo[1]
    newName = giveawayInfo[2]
    newDescription = giveawayInfo[3]
    if not checkGiveawayId(update, giveawayId): 
        return
    if not newName:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='Giveaway is missing the name')
        return
    if not newDescription:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='Giveaway is missing the description')
        return
    if (not newNoW) | (not newNoW.isdigit()):
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='Giveaway is missing the NumberOfWinners')
        return
    if int(newNoW) < 1:
        bot.sendMessage(chat_id=update.effective_chat.id,
                        text='NumberOfWinners should be greater than zero')
        return

    giveaway = loadGiveaway(giveawayId)
    giveaway.name = newName
    giveaway.description = newDescription
    giveaway.numberOfWinners = int(newNoW)
    giveaway.photoId = photo_id
    saveGiveaway(giveaway)
    makeGiveawayPost(giveaway, update)

# /chatId
def chatId(update: Update, context: CallbackContext):
    bot.sendMessage(chat_id=update.effective_chat.id,
                    text=str(update.effective_chat.id)
                    )

# Filters out unknown text
def unknown_text(update: Update, context: CallbackContext):
    reply = "Sorry I can't recognize you , you said '%s', dumb fuck" % update.message.text
    for chatRule in chatRules:
        if chatRule.check(update.message.text):
            reply = chatRule.reply()
            update.message.reply_text(reply)

# Filters out unknown commands
def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command, so go fuck yourself!" % update.message.text)

# handles messages with photos
def photoHandler(update: Update, cb: CallbackContext):
    logger.info('processing photo with caption "{0}"'.format(update.effective_message.caption))
    message = update.effective_message
    text = message.caption
    photoId = message.photo[0].file_id
    print(str(len(message.photo)))
    print([x.file_id for x in message.photo])
    print([x.file_size for x in message.photo])
    if (bool(text)) and (text.startswith('/g_create')):
        # if len(message.photo) > 1:
        #     sendMessage(update, 'Giveaway can contain only one photo')
        #     return
        giveaway_create(update, message.caption, photoId)
    if (bool(text)) and (text.startswith('/g_edit')):
        # if len(message.photo) > 1:
        #     sendMessage(update, 'Giveaway can contain only one photo')
        #     return
        giveaway_edit(update, message.caption, photoId)

# /run_test
def run_test(update :Update, cb :CallbackContext):
    chatFunc.sendMessage(update, "/g_create 1''tst''tst")
    chatFunc.sendMessage(update, "/g_create")
    chatFunc.sendMessage(update, "/g_create ''''''''")
    chatFunc.sendMessage(update, "/g_create -1''tst''tst")
    chatFunc.sendMessage(update, "/g_create -1''tst''tst")
    chatFunc.sendMessage(update, "/g_create 1''''tst")
    chatFunc.sendMessage(update, "/g_create 1''tst''")
    chatFunc.sendMessage(update, "/g_create 1''tst")
    with open('JordanPeterson.jpg', 'rb') as jordan_picture:
        bot.send_photo(chat_id=update.effective_chat.id,
                        photo = jordan_picture, 
                        caption = "/g_create 1''tst''tst")

    chatFunc.sendMessage(update, "/g_post ")
    chatFunc.sendMessage(update, "/g_post 2")
    chatFunc.sendMessage(update, "/g_post 2745cb60-a367-4bd8-9a49-054e268b35b1")

    chatFunc.sendMessage(update, "/g_subs ")
    chatFunc.sendMessage(update, "/g_subs 2")
    chatFunc.sendMessage(update, "/g_subs 2745cb60-a367-4bd8-9a49-054e268b35b1")

    chatFunc.sendMessage(update, "/g_finish ")
    chatFunc.sendMessage(update, "/g_finish 2")
    chatFunc.sendMessage(update, "/g_finish 2745cb60-a367-4bd8-9a49-054e268b35b1")

def callback_query_handler(update: Update, context: CallbackContext):
    logger.info('processing callback "{0}"'.format(update.callback_query.data))
    callbackData = update.callback_query.data
    if callbackData.startswith(SUBSCRIBE_KEYWORD):
        giveawayId = callbackData.replace(SUBSCRIBE_KEYWORD, '')
        giveaway = loadGiveaway(giveawayId)
        user = UserInfo(update)
        if giveaway.isSubbedToGiveaway(user):
            bot.sendMessage(chat_id=update.effective_chat.id,
                            text='%s is already subscribed to the giveaway' % update.effective_user.name)
        else:
            giveaway.subscribers.append(user)
            saveGiveaway(giveaway)
            bot.sendMessage(chat_id=update.effective_chat.id,
                            text='%s has been added to the giveaway subscribers' % update.effective_user.name)
        return
    if callbackData.startswith(UNSUBSCRIBE_KEYWORD):
        giveawayId = callbackData.replace(UNSUBSCRIBE_KEYWORD, '')
        giveaway = loadGiveaway(giveawayId)
        user = UserInfo(update)
        sameUser = user.findSame(giveaway.subscribers)
        if sameUser:
            giveaway.subscribers.remove(sameUser)
            saveGiveaway(giveaway)
            bot.sendMessage(chat_id=update.effective_chat.id,
                            text='%s has been unsubscribed from the giveaway' % update.effective_user.name)
            print(giveaway.isSubbedToGiveaway(sameUser))
        else:
            bot.sendMessage(chat_id=update.effective_chat.id,
                            text='%s is not in the giveaway' % update.effective_user.name)
        return
    if callbackData.startswith(INFO_KEYWORD):
        userInfo = 'userId:{0}\nuserName:{1}\nchatId:{2}'.format(
            update.effective_user.id,
            update.effective_user.username,
            update.effective_chat.id
        )
        bot.sendMessage(
            chat_id=update.effective_chat.id,
            text=userInfo
        )
        return

# inDev
def inDev(update: Update, context: CallbackContext):
    update.message.reply_text(
        "In development")

updater.dispatcher.add_handler(CommandHandler('info', info))
updater.dispatcher.add_handler(CommandHandler('restart', restart))
# create new giveaway with Description, Number of winners
# /g_create NoW''Name''Description
# /g_create 3''Annual Giveaway #3''This time we will giveaway 3 new skins to the members of community!\nAll you have to do is to press 'subscribe' button just below the post
updater.dispatcher.add_handler(CommandHandler('g_create', giveaway_createHandler)) 
# [author only] creates new giveaway post
# /g_post giveawayId
# /g_post 41cce09e-10b3-4cb2-9228-52d4d872eabc
updater.dispatcher.add_handler(CommandHandler('g_post', giveaway_post)) 
# [author only] shows number and nicknames of giveaway subs 
# /g_subs giveawayID
# /g_subs 41cce09e-10b3-4cb2-9228-52d4d872eabc
updater.dispatcher.add_handler(CommandHandler('g_subs', giveaway_subs))
# [author only] change Description, Number of winners
# /g_edit giveawayID''NoW''Name''Description   
# /g_edit 41cce09e-10b3-4cb2-9228-52d4d872eabc''3''Annual Giveaway #3''This time we will giveaway 3 new skins to the members of community!\nAll you have to do is to press 'subscribe' button just below the post
updater.dispatcher.add_handler(CommandHandler('g_edit', giveaway_editHandler))
# [author only] ends a giveaway if needed; sends a post about winners
# /g_finish giveawayID
# /g_finish 41cce09e-10b3-4cb2-9228-52d4d872eabc
updater.dispatcher.add_handler(CommandHandler('g_finish', giveaway_finish)) 
# /run_test
updater.dispatcher.add_handler(CommandHandler('run_test', run_test)) 
# /run_test
updater.dispatcher.add_handler(MessageHandler(Filters.photo, photoHandler)) 
# processes buttons requests
updater.dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CommandHandler('help', help))
# updater.dispatcher.add_handler(CommandHandler('html', html))
# updater.dispatcher.add_handler(CommandHandler('reply', reply))
# updater.dispatcher.add_handler(CommandHandler('chatId', chatId))
# updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
# updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))

if local:
    logger.info('polling messages...')
    updater.start_polling()
else:
    logger.info('setting webhook on "{0}" listening on address "{1}:{2}"...'.
                format(WEBHOOK_URL, "0.0.0.0", PORT))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=WEBHOOK_URL)
    updater.bot.set_webhook(WEBHOOK_URL)
    bot.set_webhook(WEBHOOK_URL)

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
