from typing import List
from unicodedata import name
from uuid import UUID
from config import MONGODB_CONNECTION_STRING
from giveaway import Giveaway
from pymongo import MongoClient
from userInfo import UserInfo


def get_collection():
    client = MongoClient(MONGODB_CONNECTION_STRING)
    db = client['giveaways']
    collection = db["giveaways"]
    return collection


def serialize_giveaway(giveaway: Giveaway):
    def serialize_userInfoArray(userInfoArray: List[UserInfo]):
        return list(map(lambda x:
                        {
                            "id": x.id,
                            "name": x.name
                        }, userInfoArray))
    giveaway_schema = {
        "_id": str(giveaway.id),
        "author": giveaway.author,
        "authorNick": giveaway.authorNick,
        "name": giveaway.name,
        "description": giveaway.description,
        "numberOfWinners": giveaway.numberOfWinners,
        "id": str(giveaway.id),
        "subscribers": serialize_userInfoArray(giveaway.subscribers),
        "ended": giveaway.ended,
        "winners": serialize_userInfoArray(giveaway.winners),
        "photoId": giveaway.photoId,
    }
    return giveaway_schema


def deserialize_giveaway(giveaway_info) -> Giveaway:
    def deserialize_userInfoArray(userInfoArray) -> List[UserInfo]:
        return list(map(lambda x:
                        UserInfo(
                            id=x['id'],
                            name=x['name'],
                        ), userInfoArray))
    giveaway = Giveaway(
        author=giveaway_info['author'],
        authorNick=giveaway_info['authorNick'],
        name=giveaway_info['name'],
        description=giveaway_info['description'],
        NumberOfWinners=giveaway_info['numberOfWinners'],
        id=UUID(giveaway_info['id']),
        subscribers=deserialize_userInfoArray(giveaway_info['subscribers']),
        ended=giveaway_info['ended'],
        winners=deserialize_userInfoArray(giveaway_info['winners']),
        photoId=giveaway_info['photoId'],
    )
    return giveaway


def giveaway_exists(giveawayId: str):
    collection = get_collection()
    return collection.count_documents({'_id': giveawayId}, limit=1) != 0


def get_giveaways_of_a_user(user_id: str):
    collection = get_collection()
    giveaways_info = collection.find({'author': user_id})
    giveaways = [deserialize_giveaway(giveaway_info)
                 for giveaway_info in giveaways_info]
    return giveaways


def delete_giveaway(giveawayId: str):
    collection = get_collection()
    collection.delete_one({'_id': giveawayId})
    print('giveaway "%s" deleted' % str(giveawayId))


def save_giveaway(giveaway: Giveaway):
    collection = get_collection()
    new_values = serialize_giveaway(giveaway)
    if giveaway_exists(str(giveaway.id)):
        query = {"_id": str(giveaway.id)}
        set_new_values = {"$set": new_values}
        collection.update_one(query, set_new_values)
        print('giveaway "%s" updated' % str(giveaway.id))
    else:
        collection.insert_one(new_values)
        print('giveaway "%s" created' % str(giveaway.id))


def load_giveaway(giveawayId: str) -> Giveaway:
    collection = get_collection()
    giveaway_info = collection.find_one(giveawayId)
    print('giveaway "%s" loaded' % giveawayId)
    giveaway = deserialize_giveaway(giveaway_info)
    return giveaway
