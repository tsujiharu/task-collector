# スレッド・マトメタリ

Discordチャンネル内のスレッドのタイトルと作成者でタスクリストを作るbot。

---

## 環境の準備

この手順を踏んで準備しよう：

1. botアカウントを作成（[作成方法](https://discordpy.readthedocs.io/ja/stable/discord.html)）
2. botをサーバーに招待（[招待方法](https://discordpy.readthedocs.io/ja/stable/discord.html#inviting-your-bot)）
3. botの実行環境を用意（[インストール方法](https://discordpy.readthedocs.io/ja/stable/intro.html#installing)）

招待時はこれらの権限を与えよう（BOT PERMISSIONS）：
- Send Messages
- Manage Messages
- Manage Threads
- Read Message History

### 実行環境

- OS
  - Linux・macOSなどのPOSIX環境（Windowsでも作動する確認はしていない）
- Python
  - 3.8以上
- ライブラリ（PIP）
  - `requirements.txt`の通り。インストールはこう。
    ```sh
    python3 -m pip install -U -r requirements.txt
    ```

上記の要素はDockerコンテナ内で整うものでもある。Dockerを用いる場合はこのようにDockerイメージを作成しよう。

```sh
docker build --tag task-collector .
```

---

## 起動

### shellで直接実行する場合

準備が整ったら、POSIX環境ではとりあえずこれで動くはず。

```sh
# ソースコードの保存先ディレクトリーに移動
cd task-collector/src

# 認証トークンを入力
export TASK_COL_TOKEN="<bot-token>"
# 作動するチャンネルを指定。指定しない場合は #タスクリスト
export TASK_COL_CHANNEL='タスクリスト'

# 起動
python3 ./task_collector.py
```

`python3`は環境設定によっては`python`になっているかもしれない。注意してPython 3.8以上のものを選ぼう。

`task-collector`はプロジェクトの保存先に置き換えよう。 

`<bot-token>`の取得方法は[これ](https://discordpy.readthedocs.io/ja/stable/discord.html)を参考にしよう。

環境によっては、上記のスクリプトの日本語コメントに対応できない場合がある。コピーする時はコメント抜きが無難だろう。


### Dockerを用いた場合

```sh
docker run --detach \
    --restart unless-stopped \
    --env 'TASK_COL_CHANNEL=タスクリスト' \
    --env "TASK_COL_TOKEN=$(cat token)" \
    --name task-collector \
    task-collector
```
