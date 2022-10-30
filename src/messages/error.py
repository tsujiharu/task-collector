import os
from discord import TextChannel

class MissingEnvError(Exception):
    def __init__(self, key: str):
        self.key = key

    def __str__(self) -> str:
        if os.name == 'nt':
            command = f'    set {self.key}=<value>'
        else:
            command = f"    export {self.key}='<value>'"
        
        pieces = [
            f'{self.key}の設定忘れてるぞー。このコマンドで直してみ？',
            command,
            'ちな、<value>は本物の値に置き換えな？'
        ]

        return '\n'.join(pieces)

class InvalidTokenError(Exception):
    def __str__(self) -> str:
        return 'ログインできなかったぞー。トークン合ってるかー'

class SendForbiddenError(Exception):
    def __init__(self, channel: TextChannel):
        self.channel_name = channel.name

    def __str__(self) -> str:
        return f'#{self.channel_name} にリストを送ろうとしたら弾かれたぞー。チャンネルのアクセス権限設定間違ってないかー'

class ThreadEndMisuseError(Exception):
    def __str__(self) -> str:
        return '`/$end`はスレッドで使ってくれ……。'
