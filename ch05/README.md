```sh
# 初回のみ ディレクトリ作成、プロジェクト作成
$ cd ch05/myblog
$ uv run django-admin startproject config backend/

# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env up --detach
# Docker再ビルド
$ docker compose --env-file ../../.env build

$ docker compose exec web uv run backend/manage.py migrate
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
# カスタムユーザーモデルを利用しており、ユーザーを pnohe_no で識別しているので phone_no を別途設定している
$ docker compose exec web uv run backend/manage.py createsuperuser --noinput --phone_no 08087654321
```
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/login/

```sh
$ mkdir backend/blog
$ docker compose exec web uv run django-admin startapp blog backend/blog
$ mkdir backend/author
$ docker compose exec web uv run django-admin startapp author backend/author
$ mkdir backend/helper
$ docker compose exec web uv run django-admin startapp helper backend/helper
```

### ダミーデータの登録
```sh
$ docker compose exec web uv run backend/manage.py dummy_data_register
```

### セッション
https://docs.djangoproject.com/en/5.1/topics/http/sessions/

### ユーザーモデルのカスタマイズ

1. User　モデルと1対1のモデル(例えば UserProfile モデル)を作成して拡張する.
  - シンプルでクリーンなソリューション
2. AbstractUser モデルと AbstractBaseUser モデルを使って拡張する
  - AbstractUser モデルか AbstractBaseUser モデルを継承してカスタムユーザーモデルを作成する
     - AbstractUser ... User モデルの username  フィールドを更新する場合にのみ使う
     - AbstractBaseUser ... User テーブルの「すべてのフィールドを最初から作成する場合に使用する

```sh
$ mkdir backend/custom_user
$ docker compose exec web uv run django-admin startapp custom_user backend/custom_user
```
- 完全な例
https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#a-full-example

### その他コマンド

```sh
$ docker compose exec web uv run backend/manage.py migrate
$ docker compose exec web uv run backend/manage.py makemigrations
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose exec web uv run backend/manage.py createsuperuser --noinput

# 環境変数の確認
$ docker compose exec web env
$ docker compose --env-file ../../.env exec web env
```

### ruff によるコード整形
```sh
$ docker compose exec web uv run ruff check . --fix
$ docker compose exec web uv run ruff format .
```
