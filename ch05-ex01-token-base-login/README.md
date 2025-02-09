```sh
# 初回のみ ディレクトリ移動
$ cd ch05-ex01-token-base-login/myblog

### フロントエンド
# 初回のみ プロジェクト作成
$ npx create-next-app@latest frontend/ --ts --eslint --tailwind --src-dir --use-npm --app --turbopack --no-import-alias

### バックエンド
$ uv run django-admin startproject config backend/

# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env build --no-cache
$ docker compose --env-file ../../.env up --detach

$ docker compose --env-file ../../.env exec backend uv run manage.py migrate
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose --env-file ../../.env exec backend uv run manage.py createsuperuser --noinput

# キャッシュの削除
$ docker builder prune -f
```
### フロントエンド
http://127.0.0.1:3000/
# Login ページ
http://127.0.0.1:3000/account/login
http://127.0.0.1:3000/top

### バックエンド
http://127.0.0.1:8000/account/login/
http://127.0.0.1:8000/account/logout/
http://127.0.0.1:8000/account/logoutall/

# ログインしていないと見れないユーザー情報のページ
http://127.0.0.1:8000/account/user/


```sh
$ mkdir backend/blog
$ docker compose --env-file ../../.env exec backend uv run django-admin startapp blog backend/blog
$ mkdir backend/author
$ docker compose --env-file ../../.env exec backend uv run django-admin startapp author backend/author
$ mkdir backend/helper
$ docker compose --env-file ../../.env exec backend uv run django-admin startapp helper backend/helper
$ mkdir backend/account
$ docker compose --env-file ../../.env exec backend uv run django-admin startapp account backend/account
```

### ダミーデータの登録
```sh
$ docker compose --env-file ../../.env exec backend uv run manage.py dummy_data_register
```

### django-rest-knox を使う
https://github.com/jazzband/django-rest-knox
https://jazzband.github.io/django-rest-knox/auth/

### Django と Next.js 間のデータ接続

- backend
  - django-cors-headers を導入
    - settings.py
      - INSTALL_APPS に "corsheaders" 追加
      - MIDDLEWARE に "corsheaders.middleware.CorsMiddleware" 追加
      - CORS_ORIGIN_WHITELIST = ("http://127.0.0.1/3000",) を追加
      - CORS_ALLOW_CREDENTIALS = True
  - frontend
    - fetch 時、フォームデータを Json 化する
        - const formData = new FormData(event.currentTarget);
        - const formDataJson = Object.fromEntries(formData.entries());
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formDataJson),

```sql
# テーブル一覧
select schemaname, tablename, tableowner from pg_tables;
```
- knox_authtoken テーブルの token_key カラムに トークン情報が保存されている

### トークン認証のログイン・ログアウト画面を実装

- ログイン画面
  - http://127.0.0.1:3000/account/login
- superuser の username, password でログインできる
- ログインすると、TOPページ (http://127.0.0.1:3000/top) にリダイレクトされる
- Django で作成されたトークンを, Next.js の localStorage に保存する
- 認証の有効期間は30分
  - settings.py の REST_KNOX, TOKEN_TTL で設定可能

- TOPページ
  - http://127.0.0.1:3000/top
  - Next.js の localStorage に保存されたトークンが有効であれば、username を表示する
    - ログアウトボタンを押すと、すぐにログアウトする　
  - 有効でなければ、「ユーザー情報を取得できませんでした」と表示する


### その他コマンド

```sh
# フロントエンド
# install した node_modules フォルダの削除
$ docker compose --env-file ../../.env exec frontend rm -rf node_modules

# JavaScript ライブラリのインストール
$ docker compose --env-file ../../.env exec frontend npm install

# package-json, package-json-lock のアプデ
$ docker compose --env-file ../../.env exec frontend npx npm-check-updates -u
$ docker compose --env-file ../../.env exec frontend npm install

# バックエンド
$ docker compose --env-file ../../.env exec backend uv run manage.py migrate
$ docker compose --env-file ../../.env exec backend uv run manage.py makemigrations
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose --env-file ../../.env exec backend uv run manage.py createsuperuser --noinput

# 環境変数の確認
$ docker compose --env-file ../../.env exec backend env
```

### コード整形
```sh
# フロントエンド
# ESLint の実行
$ docker compose --env-file ../../.env exec frontend npm run lint

# バックエンド
$ docker compose --env-file ../../.env exec backend uv run ruff check . --fix
$ docker compose --env-file ../../.env exec backend uv run ruff format .
```
