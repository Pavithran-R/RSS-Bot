from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from info import DATABASE_NAME, DATABASE_URI, COLLECTION_NAME

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
instance = Instance(db)


@instance.register
class RssLink(Document):
    chat_id = fields.IntField(required=True)
    title = fields.StrField(required=True)
    link = fields.StrField(required=True)
    last_update = fields.StrField(required=True)

    class Meta:
        collection_name = COLLECTION_NAME
        indexes = [{'key': ['chat_id', 'link'], 'unique': True}]


async def add_link(chat_id, title, link, last_update):
    document = RssLink(chat_id=chat_id, title=title, link=link, last_update=last_update)
    await document.commit()


async def remove_link(**kwargs):
    result = await RssLink.collection.delete_one(kwargs)
    return result.raw_result['n']


async def get_all_links(filter=None):
    if filter is None:
        filter = {}
    async for doc in RssLink.find(filter):
        yield doc