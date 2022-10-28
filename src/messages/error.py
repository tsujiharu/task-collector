import os

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
