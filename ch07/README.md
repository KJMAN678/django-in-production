```sh
# 初回のみ ディレクトリ作成、プロジェクト作成
$ cd ch07/myblog

- 前の章の pyproject.toml、docker関連ファイルを myblog ディレクトリ直下にコピーする
- 前の章の backend ディレクトリを myblog ディレクトリ直下にコピーする

$ mkdir logs
```

```sh
# ディレクトリ構成
ch07/ --- myblog/ --- backend/ --- config/
       |           |
       |           |- logs/
       |           |- docker-compose.yaml
       |           |- Dockerfile
       |           |- pyproject.toml
       |           |- uvlock.lock
       |
       |- README.md
```

```sh
# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env up --detach
# Docker再ビルド
$ docker compose --env-file ../../.env build

$ docker compose --env-file ../../.env exec web uv run backend/manage.py migrate
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
# カスタムユーザーモデルを利用しており、ユーザーを pnohe_no で識別しているので phone_no を別途設定している
$ docker compose --env-file ../../.env exec web uv run backend/manage.py createsuperuser --noinput

# ダミーデータの登録
$ docker compose --env-file ../../.env exec web uv run backend/manage.py dummy_data_register

# キャッシュの削除
$ docker builder prune -f
```
- author_id が 1のブログを取得
http://127.0.0.1:8000/blog/blogs_auto_invalidation/?author_id=1
http://127.0.0.1:8000/blog/blogs_anon_view/
http://127.0.0.1:8000/blog/blogs_user_view/
http://127.0.0.1:8000/blog/blogs_scoped_view/

- def log_event() でログを記録する
http://127.0.0.1:8000/blog/blogs_logs/?author_id=1

- ページネーション比較用, ページネーションのないブログ一覧
http://127.0.0.1:8000/blog/unpaginated/
- ページネーションのあるブログ一覧
http://127.0.0.1:8000/blog/paginated/?page=1&page_size=1
- DjangoのPagenatorを使ったページネーションのあるブログ一覧
http://127.0.0.1:8000/blog/django_paginator/?page=1&page_size=1

- DRFのページネーション
http://127.0.0.1:8000/blog/get_blogs/?limit=10&offset=1

- custom signal
http://127.0.0.1:8000/blog/publish?id=1

- admin画面
http://127.0.0.1:8000/admin/login/


### ページネーション

- [Django 公式ドキュメント Pagination](https://docs.djangoproject.com/en/5.1/topics/pagination/)

- [Django RESTFramework Pagination](https://www.django-rest-framework.org/api-guide/pagination/)
  - [PageNumberPagination](https://www.django-rest-framework.org/api-guide/pagination/#pagenumberpagination)
    - URLクエリパラメーターとして、ページ番号を送信する
  - [LimitOffsetPagination](https://www.django-rest-framework.org/api-guide/pagination/#limitoffsetpagination)
    - レスポンスでフェッチするエントリーの数と、データをフェッチできるオフセットの数を送信する
    - よりデータ取得を詳細に制御できるが、APIに脆弱性をもたらす可能性もある
      - limit を悪意を持って膨大な数を設定されるとサーバーに負荷がかかるので、非現実的な limit を設定された場合は、制限をかける必要がある.
  - [CursorPagination](https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination)
    - ページ番号ではなく、位置情報（カーソル）を使う.
    - 大規模システムでページネーションを実装するためのスケーラブルな手法.
    - 設計思想については[こちらの記事参照](https://cra.mr/2011/03/08/building-cursors-for-the-disqus-api/)
      - LIMIT/OFFSET は大きな結果セットでは非常に低速
    - ChatGPTによる補足
      - PageNumberPagination の問題点：順序の変動による結果のズレ
        - PageNumberPagination は、ページ番号を指定してデータを取得する方式です。例えば、?page=2 と指定すると、2ページ目のデータを取得します。
        - 問題点：
          - データの追加・削除によるズレ： データが頻繁に追加・削除される環境では、ページ番号による指定が不安定になる可能性があります。
        - 具体例：
          - 初回リクエスト： 1ページあたり10件のデータを取得する設定で、?page=2 をリクエストすると、11番目から20番目のデータが返されます。
        - データの追加： その後、新しいアイテムが5つ追加され、全体のデータが5つ前にシフトします。
          - 再度リクエスト： 同じく ?page=2 をリクエストすると、16番目から25番目のデータが返されます。
        - CursorPagination は、カーソル（位置情報）を使用してデータを取得する方式です。カーソルは、現在の位置を示すトークンとして機能します。
          - 利点：
            - 順序の安定性： データの追加や削除があっても、カーソルは特定の位置を指しているため、結果の重複や欠落が起こりにくい。

- settings.py に下記の設定を行う
  - 下記の例は LimitOffsetPagination としているが、PageNumberPagination や CursorPagination も可能
  - [カスタムのページネーション](https://www.django-rest-framework.org/api-guide/pagination/#modifying-the-pagination-style) を作成し、settings.py や views.py 内で指定することも可能.
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}
```
- views.py で下記の実装を行う
```python
class GetBlogsView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
```
- ページサイズ1、1ページ目
http://127.0.0.1:8000/blog/get_blogs/?limit=1&offset=0
- ページサイズ1、2ページ目
http://127.0.0.1:8000/blog/get_blogs/?limit=1&offset=1

https://cra.mr/2011/03/08/building-cursors-for-the-disqus-api/

### Django Signals

- Django Signalsは特定のイベントが発生した際に分離されたアプリケーションへ通知を受け取れるようにする機能
  - [参考記事 DjangoなSignalについて](https://nmomos.com/tips/2019/07/12/django-signal/)
  - [Django 公式ドキュメント シグナル](https://docs.djangoproject.com/ja/5.1/topics/signals/)

- Model Signals
  - なんらかのデータベース操作が実行されてようとしている、またはすでに実行されている場合に、開発者がアクションをトリガーするのに役立つデータベースアクションシグナル
    - pre_save / post_save
      - モデルの save() メソッドが呼び出される前と後にトリガーされる
      - update() メソッドが使用されたときにはトリガーされない
    - pre_delete / post_delete
      - Model object または queryset から delete() が呼び出される前と後にトリガーされる
    - m2m_changed
      - Django Model の ManyToManyField が変更されたときにトリガーされる
      - モデルの変更があるたびに m2m_changed がトリガーされる
      - m2m_changed によって送信される引数は以下の通り
      - pre_add / post_add
        - 1つ以上のオブジェクトが ManyToManyFiled のリレーションシップに追加される後と前に送信される
      - pre_remove / post_remove
        - 1つ以上のオブジェクトが ManyToManyFiled のリレーションシップから削除される後と前に送信される
      - pre_clear
        - ManyToManyField が クリアされる後と前に送信される
- Management Signals
  - `manage.py migrate`コマンドを実行すると起動する
  - 例えば、新しい migration change が行われる際に開発チームに通知するなど.
  - pre_migrate
    - migration プロセスの開始時に起動
  - post_migrate
    - migration プロセスが完了した後に実行

- Request / Response Signals
  - Django アプリケーションがリクエストを受信した時、およびレスポンスが処理されてクライアントに送り返されたときに発生する
  - request_started
    - Django がクライアントからシグナルを受信して処理を開始したときに送信される
  - request_finished
    - Django が HTTP レスポンスをクライアントに配信するときに送信される
  - got_request_exception
    - Django が request / response サイクルで例外に遭遇するたびにトリガーされる
- Database Wrapper
  - Django がデータベースに接続するたびにトリガーされる
  - connection_created
    - Django サーバーとデータベースの間にデータベース接続が確立されるたびに起動する

### Custom Signal

- たとえば、ユーザーが自社のWebサイトで製品を購入するたびに、電子メール、SMS、WhatsAppなどの複数の通信を送信する場合は、Custom Signal を会してそれを行うことができる
  - 購入のたびに Custom Signal を発送し、reciever を発送する

- signal の定義
- trigger
- reciever
- アプリがロードされるときに、receiver が登録されていることを確認する必要がある

### その他コマンド

### 本番環境で Signals を使う場合の注意点

```sh
$ docker compose --env-file ../../.env exec web uv run backend/manage.py migrate
$ docker compose --env-file ../../.env exec web uv run backend/manage.py makemigrations
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose --env-file ../../.env exec web uv run backend/manage.py createsuperuser --noinput

# app 追加. settings の INSTALLED_APPS も更新
$ mkdir backend/blog
$ docker compose --env-file ../../.env exec web uv run django-admin startapp blog backend/blog

# 環境変数の確認
$ docker compose --env-file ../../.env exec web env

# コンテナに入る
$ docker container exec -it web bash
```

### ruff によるコード整形
```sh
$ docker compose --env-file ../../.env exec web uv run ruff check . --fix
$ docker compose --env-file ../../.env exec web uv run ruff format .
```
