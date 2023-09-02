from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv('API_ID','18770647'))
API_HASH = getenv('API_HASH','ed11b8af8b51418dbac60b456d1429a7')
BOT_TOKEN = getenv('BOT_TOKEN','5520008350:AAHCPF2KQaRs2Y2n9OcfuiGEFesd1l15yMw')
MONGO_DB_URL = getenv('MONGO_DB_URL','mongodb+srv://PRIME:Ricks_2005@cluster0.koprs84.mongodb.net/?retryWrites=true&w=majority')
SUPPORT_CHAT = getenv('SUPPORT_CHAT','RatatoskSupport')
UPDATES_CHANNEL = getenv('UPDATES_CHANNEL','MikuNakanoXUpdates')
OWNER_ID = int(getenv('OWNER_ID','6393014348'))
LOG_CHANNEL_ID = int(getenv('LOG_CHANNEL_ID','-1001805033582'))
DEV_USERS = list(map(int, getenv("DEV_USERS", "5565211830").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "1811267624").split()))
ARQ_API_KEY = getenv('ARQ_API_KEY','DARMXR-EKRMBT-BHPDOP-UASHHF-ARQ')
DONATION_LINK = getenv('DONATION_LINK','https://t.me/ImmortalsXKing')
SUPER_USERS = DEV_USERS + SUDO_USERS
if OWNER_ID not in DEV_USERS:
    DEV_USERS.append(OWNER_ID)
if OWNER_ID not in SUPER_USERS:
    SUPER_USERS.append(OWNER_ID)
SESSION = getenv("SESSION" , "BQCLb5wc6C6D3y2QfymPHNMjDDPX-7zeybsqY5C33CDhumCynBoNAvk0_qn3ubklw7-NSMMc-45Tp_dqH35kK9cmFq2MVGxJookn2yC4d0pTDre7sEi0phvemW0lb3L0VtfHuA2tomZhyD0NCV5ZG9uZmAHAoNZyHHruGVSiXy3xPC5fkSeLjWddHzcRlOcecY0lVdhOEyFM-T1e2GAeyhKBMSsshVWY26cR3UqIUr4P8gLv4-RZxsskdBK3_Kkj5SeK1UWPbL66cqirIFc7RRVVSwZ3anpgcnHk_lWUb41ryDYgUskt-t_k3N2VVFMsf9K6yGj0vXbt-CK6yEClibIbAAAAAWfvHe4A")
    

