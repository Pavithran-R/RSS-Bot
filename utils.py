import feedparser


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (((str(days) + " days, ") if days else "") +
           ((str(hours) + " hours, ") if hours else "") +
           ((str(minutes) + " minutes, ") if minutes else "") +
           ((str(seconds) + " seconds, ") if seconds else "") +
           ((str(milliseconds) + " milliseconds, ") if milliseconds else ""))
    return tmp[:-2]


async def get_rss(url, session):
    async with session.get(url) as response:
        content = await response.text()
        return feedparser.parse(content)