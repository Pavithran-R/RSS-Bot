import os

API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']

DATABASE_URI = os.environ['DATABASE_URI']
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'rss')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'users')

DELAY = int(os.environ.get('DELAY', 3600))

HELP = """**RSS feed bot**

After successfully adding a RSS link, the bot starts fetching the feed every \
{}. Titles are used to easily manage RSS feeds and need to contain only one word.

**Commands:**
/help - Posts this help message" 
/add - title http://www\.RSS\-URL\.com" 
/remove - Title removes the RSS link" 
/list - Lists all the titles and the RSS links from the DB" 
/test - Inbuilt command that fetches a post from Reddits RSS." 
"""