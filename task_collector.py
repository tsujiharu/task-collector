import discord, os, sys, logging
from messages import info
from messages.error import *
from processing import constants
from processing import channel as channel_processing

##################
# グローバル変数 #
##################

client = discord.Client(intents=constants.INTENTS)

target_channel_name = os.getenv(constants.CHANNEL, constants.DEFAULT_TARGET_CHANNEL)
"""botが作動するチャンネル名"""

oauth_token = os.getenv(constants.OAUTH_TOKEN)
"""botの認証トークン"""


################
# イベント処理 #
################

async def update(channel):
    if isinstance(channel, discord.TextChannel) and target_channel_name == channel.name:
        await channel_processing.update_last_message(client, channel)

@client.event
async def on_ready():
    info.print_user_login(client.user)
    info.print_target_channel(target_channel_name)

    for guild in client.guilds:
        for channel in guild.text_channels:
            await update(channel)

@client.event
async def on_thread_create(thread: discord.Thread):
    await update(thread.parent)

@client.event
async def on_raw_thread_update(event: discord.RawThreadUpdateEvent):
    channel = client.get_channel(event.parent_id)
    await update(channel)

@client.event
async def on_raw_thread_delete(event: discord.RawThreadDeleteEvent):
    channel = client.get_channel(event.parent_id)
    await update(channel)

@client.event
async def on_raw_message_delete(event: discord.RawMessageDeleteEvent):
    if event.cached_message is not None:
        if event.cached_message.author.id == client.user.id:
            return
    
    channel = client.get_channel(event.channel_id)
    if isinstance(channel, discord.Thread):
        channel = channel.parent
    await update(channel)


##############
# メイン処理 #
##############

def validate_environment():
    if oauth_token is None:
        raise MissingEnvError(constants.OAUTH_TOKEN)

def main():
    try:
        validate_environment()
        client.run(oauth_token, log_level=logging.INFO)
    except discord.LoginFailure:
        raise InvalidTokenError()
    except Exception as e:
        print(e, file=sys.stderr)
        exit(-1)

if __name__ == "__main__":
    main()
