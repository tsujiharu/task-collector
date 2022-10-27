# スレッド・マトメタリ

Discordチャンネル内のスレッドのタイトルと作成者でタスクリストを作るbot。

## 起動

POSIX（Linux・macOS似）ではとりあえずこれで動くはず。

```sh
# discord.pyをインストール
python3 -m pip install -U discord.py

# プロジェクトの保存先ディレクトリーに移動。
cd task-collector

# botの認証トークンを入力
export TASK_COL_TOKEN="<bot-token>"
# 作動するチャンネルを指定。指定しない場合は #タスクリスト。
export TASK_COL_CHANNEL='タスクリスト'

# 起動
python3 ./task_collector.py
```

`task-collector`はプロジェクトの保存先に置き換えよう。  
`<bot-token>`の取得方法は[ここ](https://discordpy.readthedocs.io/ja/stable/discord.html)を参考にしよう。

環境によっては、上記のスクリプトの日本語コメントに対応できない場合がある。コピーする時はコメント抜きが無難。