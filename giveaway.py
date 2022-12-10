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

    def isSubbedToGiveaway(self, user: UserInfo):
        return any(map(user.isSame, self.subscribers))

    def isSubbedToChannel(self, bot, chat_id: str, user_id: str):
        chat_id = "-1001613537030"
        mem = bot.get_chat_member(chat_id, user_id)
        print(mem.status)
        if mem.status == 'member':
            return True
        else:
            return False

    def onlySubbedToChannel(self, bot, chat_id: str, all_subs: List[UserInfo]):
        return [sub for sub in all_subs if self.isSubbedToChannel(bot, chat_id, sub.id)]

    def reroll_user(self, bot, user_id: str):
        # get not winner subs
        not_winners_subbed_to_channel = self.onlySubbedToChannel(
            bot, "chat_id", self.subscribers)
        for winner in self.winners:
            if winner in not_winners_subbed_to_channel:
                not_winners_subbed_to_channel.remove(winner)
        # find and replace winner
        self.winners = [random.choice(not_winners_subbed_to_channel)
                        if (winner_info.id == user_id) | (winner_info.name == user_id)
                        else winner_info
                        for winner_info in self.winners]

    def endGiveaway(self, bot):
        # if subs.len < numOfWin => numOfWinners = subs.len
        actual_number_of_winners = min(
            self.numberOfWinners, len(self.subscribers))
        # generate winners
        subs = self.onlySubbedToChannel(bot, "chat_id", self.subscribers)
        print("possible subs: %s" % str(len(subs)))
        winners: List[UserInfo] = list()
        for i in range(0, actual_number_of_winners):
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
