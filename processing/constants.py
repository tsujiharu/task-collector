from discord import Intents
############
# 起動関連 #
############
CHANNEL = 'TASK_COL_CHANNEL'
TOKEN = 'TASK_COL_TOKEN'


####################
# クライアント関連 #
####################

def get_intents() -> Intents:
    intents = Intents.none()
    intents.guilds = True
    intents.messages = True
    intents.message_content = True
    return intents

INTENTS = get_intents()


################
# デフォルト値 #
################
DEFAULT_TARGET_CHANNEL = 'タスクリスト'
