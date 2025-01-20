## Poetry による仮想環境の作成

```sh
# 初期化して pyproject.toml を追加
poetry init

# ライブラリのインストール
poetry install

# ライブラリ等のアップデート
poetry update

# Python のバージョン変更 (ex. 3.10.13)
poetry env use 3.10.13

# ライブラリを pyproject.toml に追加
poetry add <library name>

# ライブラリを pyproject.toml から除去
poetry remove <library name>

# 仮想環境の有効化
poetry shell

# 仮想環境の終了
exit

# 仮想環境を立ち上げずに python の実行
poetry run python xxx.py
```
```

- [Poetry document](https://cocoatomo.github.io/poetry-ja/cli/)

## venv による仮想環境の作成

```sh
# 仮想環境の作成
python3 -m venv .venv

# 仮想環境のアクティベート
source .venv/bin/activate

# pip のアップグレード
python3 -m pip install --upgrade pip

# pip tools のインストール
pip install pip-tools

# requirements.in を更新

# 実行時の最新バージョン番号を指定した requirements.txt の生成
pip-compile requirements.in

# ライブラリのインストール
pip install -r requirements.txt
```

## Docker

```sh
# コンテナの起動
docker-compose up -d --build

# コンテナの停止
docker-compose down

# コンテナに入る
docker compose exec poetrytest bash

# コンテナから出る
exit
```

### リンター(ruff) ・ テスト (pytest) スクリプトの実行

```sh
./test.sh
```
