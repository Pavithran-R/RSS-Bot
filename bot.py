import aiohttp
from pyrogram import Client, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from marshmallow.exceptions import ValidationError

from info import API_ID, API_HASH, BOT_TOKEN, DELAY, HELP
from database import add_link, get_all_links, remove_link
from utils import time_formatter, get_rss

bot = Client('Rss bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start'))
async def start(bot, message):
    """start command"""
    await message.reply("**Hi, I'm RSS feed bot**\n\nCheck /help")


@bot.on_message(filters.command('help'))
async def help(bot, message):
    """help command"""
    await message.reply(HELP.format(time_formatter(DELAY * 1000), message.chat.id), quote=True)


@bot.on_message(filters.command('test'))
async def test(bot, message):
    """test command"""
    url = "https://github.com/pyrogram/pyrogram/releases.atom"
    async with aiohttp.ClientSession() as session:
        rss_data = await get_rss(url, session)
        title = rss_data.entries[0]['title']
        update = rss_data.entries[0]['link']
    await message.reply(f"{title}\n\n{update}", quote=True)


@bot.on_message(filters.command('list'))
async def list_cmd(bot, message):
    """list command"""
    total = 0
    async for document in get_all_links():
        await message.reply(
            f"<b>Title:</b> {document.title}\n"
            f"<b>rss url:</b> {document.link}\n"
            f"<b>Last update:</b> {document.last_update}\n",
            parse_mode='html',
            disable_web_page_preview=True)
        total += 1

    if not total:
        await message.reply('You have not added any rss link.', quote=True)


@bot.on_message(filters.command('add'))
async def add(bot, message):
    """add command"""
    try:
        link = message.command[1]
    except IndexError:
        await message.reply("The format needs to be: /add http://www.URL.com")
        return

    try:
        async with aiohttp.ClientSession() as session:
            rss_data = await get_rss(link, session)
            title = rss_data.entries[0]['title']
            update = str(rss_data.entries[0]['link'])
    except IndexError:
        await message.reply("The link does not seem to be a RSS feed or is not supported")
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)
    else:
        try:
            await add_link(message.chat.id, title, link, update)
        except ValidationError:
            await message.reply('This link is already added!', quote=True)
        except Exception as e:
            await message.reply(f"Error: {e}", quote=True)
        else:
            await message.reply(f"<b>Added</b> - {title}\n\n{update}",
                                parse_mode="html",
                                quote=True)


@bot.on_message(filters.command('remove'))
async def remove(bot, message):
    """remove command"""
    try:
        link = message.command[1]
    except IndexError:
        await message.reply("The format needs to be: /remove link")
        return

    removed = await remove_link(chat_id=message.chat.id, link=link)
    if removed:
        await message.reply(f'Removed: {link}', quote=True)
    else:
        await message.reply('There is no such rss link found!', quote=True)


async def check_updates():
    async with aiohttp.ClientSession as session:
        async for document in get_all_links():
            rss_data = await get_rss(document.link, session)
            title = rss_data.entries[0]['title']
            update = str(rss_data.entries[0]['link'])

            if (document.last_update != update):
                document.last_update = update
                await document.commit()
                await bot.send_message(chat_id=document.chat_id, text=f"{title}\n\n{update}")


scheduler = AsyncIOScheduler()
scheduler.add_job(check_updates, "interval", seconds=DELAY)

scheduler.start()
bot.run()