import random
from typing import List
from uuid import UUID
from userInfo import UserInfo


class Giveaway(object):

    def __init__(self, author: int, authorNick: str, name: str, description: str, NumberOfWinners: int, id: UUID, subscribers: List[UserInfo], ended: bool, winners: List[UserInfo], photoId: str):
        self.author = author
        self.authorNick = authorNick
        self.name = name
        self.description = description
        self.numberOfWinners = NumberOfWinners
        self.id = id
        self.subscribers = subscribers
        self.ended = ended
        self.winners = winners
        self.photoId = photoId

    def containsUser(self, user: UserInfo):
        return any(map(user.isSame, self.subscribers))

    def is_subscribed(self, bot, chat_id: str, user_id: str):
        try:
            chat_id = "-1001613537030"
            mem = bot.get_chat_member(chat_id, user_id)
            if mem.status == 'member':
                return True
            else:
                return False
        except:
            return False

    def parse_subs(self, bot, chat_id: str, all_subs: List[UserInfo]):
        subbed_subs = [
            sub for sub in all_subs if self.is_subscribed(bot, chat_id, sub.id)]
        return subbed_subs

    def endGiveaway(self, bot):
        # if subs.len < numOfWin => numOfWinners = subs.len
        self.numberOfWinners = min(self.numberOfWinners, len(self.subscribers))
        # generate winners
        subs = self.parse_subs(bot, "chat_id", self.subscribers)
        print("possible subs: %s" % str(len(subs)))
        winners: List[UserInfo] = list()
        for i in range(0, self.numberOfWinners):
            newWinner = random.choice(subs)
            subs.remove(newWinner)
            winners.append(newWinner)
        # end giveaway
        self.ended = True
        self.winners = winners

    def getWinners(self) -> List[UserInfo]:
        if not self.ended:
            self.endGiveaway()
        return self.winners

    def is_Author(self, user_id: int) -> bool:
        return self.author == user_id
