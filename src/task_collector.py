import discord, os, sys, logging
from discord import app_commands
from messages import info
from messages.error import *
from processing import comparison, constants
from processing import channel as channel_processing

##################
# グローバル変数 #
##################

client = discord.Client(intents=constants.INTENTS)

command_tree = app_commands.CommandTree(client)
"""botが受け付けるコマンドを溜める場所"""

target_channel_name = os.getenv(constants.CHANNEL, constants.DEFAULT_TARGET_CHANNEL)
"""botが作動するチャンネル名"""

token = os.getenv(constants.TOKEN)
"""botの認証トークン"""


################
# イベント処理 #
################

async def update(channel):
    if isinstance(channel, discord.TextChannel) and target_channel_name == channel.name:
        await channel_processing.update_last_message(client, channel)

async def remove_end_marker(event: discord.RawThreadUpdateEvent, channel: discord.TextChannel):
    """
    アーカイブされたスレッドが復活させられる時に、スレッド終了マーカーを削除する。
    """
    archived = False
    try:
        archived = event.data['thread_metadata']['archived']
    except KeyError:
        return

    unarchiving = event.thread is None and not archived
    if unarchiving:
        thread = None
        for t in channel.threads:
            if t.id == event.thread_id:
                thread = t
                break

        if thread is not None:
            last_message = await channel_processing.find_last_message(
                thread,
                user_id=client.user.id,
                content=constants.MARKER_PREFIX + constants.COMMAND_END,
                content_comparison=comparison.Equals()
            )
            if last_message is not None:
                await last_message.delete()

@client.event
async def on_ready():
    info.print_user_login(client.user)

    await command_tree.sync()
    info.print_command_tree_synced()

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
    await remove_end_marker(event, channel)
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

################
# コマンド処理 #
################

@command_tree.command(name=constants.COMMAND_END, description='タスクが終わったらこれで知らせてくれ')
async def on_task_end(interaction: discord.Interaction):
    channel = interaction.channel
    if isinstance(channel, discord.Thread):
        thread = channel
        await interaction.response.send_message(constants.MARKER_PREFIX + constants.COMMAND_END)
        await thread.edit(archived=True)
    else:
        await interaction.response.send_message(ThreadEndMisuseError())

##############
# メイン処理 #
##############

def validate_environment():
    if token is None:
        raise MissingEnvError(constants.TOKEN)

def main():
    try:
        validate_environment()
        client.run(token, log_level=logging.INFO)
    except discord.LoginFailure:
        raise InvalidTokenError()
    except Exception as e:
        print(e, file=sys.stderr)
        exit(-1)

if __name__ == "__main__":
    main()
