from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv('API_ID','18770647'))
API_HASH = getenv('API_HASH','ed11b8af8b51418dbac60b456d1429a7')
BOT_TOKEN = getenv('BOT_TOKEN','5520008350:AAFoHHVAlYnyEkqWzEVnk0r9a3Yy44CV-H8')
MONGO_DB_URL = getenv('MONGO_DB_URL','mongodb+srv://PRIME:Ricks_2005@cluster0.koprs84.mongodb.net/?retryWrites=true&w=majority')
SUPPORT_CHAT = getenv('SUPPORT_CHAT','RatatoskSupport')
UPDATES_CHANNEL = getenv('UPDATES_CHANNEL','MikuNakanoXUpdates')
OWNER_ID = int(getenv('OWNER_ID','6393014348'))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID','-1001805033582'))
DEV_USERS = list(map(int, getenv("DEV_USERS", "5565211830").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "1811267624").split()))
ARQ_API_KEY = getenv('ARQ_API_KEY','DARMXR-EKRMBT-BHPDOP-UASHHF-ARQ')
DONATION_LINK = getenv('DONATION_LINK','https://t.me/ImmortalsXKing')
if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)

