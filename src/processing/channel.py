from typing import Optional
from discord import Client, TextChannel, Message, NotFound
from messages import info
from messages.error import SendForbiddenError

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

async def find_last_message(channel: TextChannel, user_id: Optional[int] = None) -> Optional[Message]:
    """
    最大30件のメッセージを遡って、`channel`で最後に送られたメッセージを返す。
    `user_id`を指定した場合は、そのユーザーが最後に送ったメッセージを探して返す。
    見つからなかった場合は`None`を返す。
    """
    last_message = None
    async for m in channel.history(limit=30, oldest_first=False):
        if user_id is None or m.author.id == user_id:
            if last_message is None or m.created_at > last_message.created_at:
                last_message = m
    return last_message

async def update_last_message(client: Client, channel: TextChannel):
    """
    まとめリストを`channel`に送る。
    このbotが`channel`で既存のメッセージがあった場合は削除する。
    """
    message = await build_message(channel)
    info.print_message_built(channel.name)

    last_message = await find_last_message(channel, user_id=client.user.id)

    if last_message is not None:
        await last_message.delete()

    try:
        await channel.send(content=message)
    except Forbidden:
        raise SendForbiddenError()
    
    info.print_message_sent(channel.name)
