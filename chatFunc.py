from telegram.bot import Bot
from telegram.update import Update
from giveaway import Giveaway
from locals import get_line


class ChatFunc(object):

    def __init__(self, bot: Bot):
        self.bot = bot

    def sendMessage(self, update: Update, message: str):
        self.bot.send_message(chat_id=update.effective_chat.id,
                              text=message)

    def deleteOriginalMessage(self, update: Update):
        if not update.message:
            self.bot.delete_message(chat_id=update.channel_post.chat_id,
                                    message_id=update.channel_post.message_id
                                    )
            return
        self.bot.deleteMessage(chat_id=update.message.chat_id,
                               message_id=update.message.message_id
                               )

    def sendDontHavePermission(self, update: Update, giveaway: Giveaway, langId: int):
        self.bot.sendMessage(chat_id=update.effective_chat.id,
                             text=get_line(langId, 'err_no_access') % giveaway.authorNick)

    def isChatWithAuthor(self, update: Update, giveaway: Giveaway):
        return (update.effective_user.id == giveaway.author) & (update.effective_chat.id == giveaway.author)
