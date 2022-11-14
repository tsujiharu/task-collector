import asyncio
from processing import constants
from processing.comparison import Comparison
from typing import Optional, Union
from discord import Client, TextChannel, Thread, Message, NotFound, Forbidden
from messages import info
from messages.error import SendForbiddenError

_unarchive_update_locks = {}

async def unarchive_all_archived_threads(channel: TextChannel) -> bool:
    """
    `channel`の中の、`$end`で終わっていないスレッドをすべて復活させる。
    """
    lock = _unarchive_update_locks.get(channel.id)
    if lock is None:
        lock = asyncio.Lock()
        _unarchive_update_locks[channel.id] = lock

    await lock.acquire()

    async for thread in channel.archived_threads(limit=None):
        last_message = None
        async for message in thread.history(limit=1):
            last_message = message

        if last_message is not None:
            ended = last_message.content.__contains__(constants.MARKER_PREFIX + constants.COMMAND_END)
            if not ended:
                await thread.edit(archived=False)

    lock.release()

async def build_message(channel: TextChannel) -> str:
    """
    `channel`の中からアクティブのスレッド名をすべて集めて、タスクリストの文面を作って返す。
    """
    if channel.threads.__len__() == 0:
        return '\n'.join(['タスクはもう残ってないみたいだぞー', 'やったな'])

    message_pieces = ['**タスク（古い順）**']

    # この関数の中だけで生きる、古い順のthreadsを作る
    threads = channel.threads.copy()
    threads.sort(key=lambda t : t.created_at)

    for thread in threads:
        title = thread.name
        try:
            starter_message = await channel.fetch_message(thread.id)
            proposer = starter_message.author
            message_pieces.append(f'- {title} ({proposer.display_name})')
        except NotFound:
            message_pieces.append(f'- {title}')

    return '\n'.join(message_pieces)

async def delete_latest_messages(
    channel: Union[TextChannel, Thread],
    user_id: int
):
    """
    `channel`で最後に送られたメッセージを削除する。
    `user_id`を指定した場合は、そのユーザーが最後に送ったメッセージを探して削除する。
    見つからなかった場合は`None`を削除する。
    """
    earliest_created_at = None
    exhausted = False
    while not exhausted:
        iter = channel.history(limit=constants.HISTORY_FETCH_SIZE, before=earliest_created_at)
        messages = [m async for m in iter]
        for m in messages:
            if earliest_created_at is None or m.created_at < earliest_created_at:
                earliest_created_at = m.created_at
            if m.author.id != user_id:
                continue
            await m.delete()
        exhausted = (messages.__len__() < constants.HISTORY_FETCH_SIZE)

async def update_last_message(client: Client, channel: TextChannel):
    """
    まとめリストを`channel`に送る。
    このbotが`channel`で既存のメッセージがあった場合は削除する。
    """
    await unarchive_all_archived_threads(channel)

    message = await build_message(channel)
    info.print_message_built(channel.name)

    await delete_latest_messages(channel, client.user.id)

    try:
        await channel.send(content=message)
    except Forbidden:
        raise SendForbiddenError()
    
    info.print_message_sent(channel.name)
