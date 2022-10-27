# スレッド・マトメタリ
Discordチャンネル内のスレッドのタイトルと作成者でタスクリストを作るbot。

# 実行

POSIX（Linux・macOS似）ではとりあえずこれで動くはず。

```sh
python3 -m pip install -U discord.py

cd task-collector

export TOKEN="<bot-token>"
python3 ./task_collector.py
```

`<bot-token>`の取得は[ここ](https://discordpy.readthedocs.io/ja/stable/discord.html)を参考にしよう。  
`task-collector`はプロジェクトの保存先に置き換えよう。
