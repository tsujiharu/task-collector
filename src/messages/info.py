import logging

def logger():
    """discord.py内蔵のロガーを返す。"""
    return logging.getLogger('discord')

def print_user_login(username: str):
    """ログイン成功を記録"""
    logger().info(f'{username}としてログインしてやったぞー')

def print_command_tree_synced():
    """アプリコマンドをdiscordサーバーに同期したことを記録"""
    logger().info('使えるコマンドを鯖に知らせといたからなー')

def print_target_channel(target_channel: str):
    """指定チャンネルを記録"""
    logger().info(f'仕事は #{target_channel} でするんだな？　あいよー')

def print_message_built(channel_name: str):
    """まとめメッセージの構築完了を記録"""
    logger().debug(f'{channel_name}でまとめを作っといたぞー')

def print_message_sent(channel_name: str):
    """指定チャンネルでまとめメッセージの送信を記録"""
    logger().debug(f'{channel_name}でまとめを送ってやったぞー')

def print_message_edited(channel_name: str):
    """指定チャンネルでまとめメッセージの編集を記録"""
    logger().debug(f'{channel_name}でまとめをアプデしてやったぞー')
