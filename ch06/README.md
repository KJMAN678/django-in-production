```sh
# 初回のみ ディレクトリ作成、プロジェクト作成
$ cd ch06/myblog
$ uv run django-admin startproject config backend/

# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env up --detach
# Docker再ビルド
$ docker compose --env-file ../../.env build

$ docker compose --env-file ../../.env exec web uv run backend/manage.py migrate
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
# カスタムユーザーモデルを利用しており、ユーザーを pnohe_no で識別しているので phone_no を別途設定している
$ docker compose --env-file ../../.env exec web uv run backend/manage.py createsuperuser --noinput

# キャッシュの削除
$ docker builder prune -f
```
- author_id が 1のブログを取得
http://127.0.0.1:8000/blog/blogs/?author_id=1
http://127.0.0.1:8000/blog/blogs_auto_invalidation/?author_id=1
http://127.0.0.1:8000/blog/blogs_anon_view/
http://127.0.0.1:8000/blog/blogs_user_view/
http://127.0.0.1:8000/blog/blogs_scoped_view/

http://127.0.0.1:8000/admin/login/


```sh
$ mkdir backend/blog
$ docker compose --env-file ../../.env exec web uv run django-admin startapp blog backend/blog
$ mkdir backend/author
$ docker compose --env-file ../../.env exec web uv run django-admin startapp author backend/author
$ mkdir backend/helper
$ docker compose --env-file ../../.env exec web uv run django-admin startapp helper backend/helper
$ mkdir backend/common
$ docker compose --env-file ../../.env exec web uv run django-admin startapp common backend/common
```

### ダミーデータの登録
```sh
$ docker compose --env-file ../../.env exec web uv run backend/manage.py dummy_data_register
```

### Cache の確認コマンド
```sh
$ docker compose --env-file ../../.env exec web uv run backend/manage.py print_cache
```
- ビューごとのキャッシュ
https://docs.djangoproject.com/en/5.1/topics/cache/#the-per-view-cache
- Django RestFramework Caching
https://www.django-rest-framework.org/api-guide/caching/

### django-cacheops
https://github.com/Suor/django-cacheops
- ORM クエリを自動キャッシュしてくれたり, 色々キャッシュ周りを自動化してくれるらしい.

- invalidate でキャッシュを削除することもできる
https://github.com/Suor/django-cacheops?tab=readme-ov-file#invalidation

```python
# author ID 12 のキャッシュを削除
get_all_blogs.invalidate(12)

# すべてキャッシュを削除
get_all_blogs.invalidate()
```

### 本番環境でキャッシュを実装する場合の注意点
- 本番環境でキャッシュを実装する場合は、可用性の高い Redis クラスターを使うこと
- AWS の ElasticCache や Redis Lab などのマネージド・サービスを使い、マスター・スレーブ構成を使用すること
  - マスター・スレーブ構成とは、複数の機器やシステムを連携して動作させる際に、1つをマスター、残りをスレーブとして役割分担する方式
- 読み取りの多いシステムでキャッシュがダウンすると、すべての読み取りクエリがデータベースにヒットし、カスケード効果が発生してシステム全体がダウンする可能性があるため.

### Django での スロットリング
- スロットリングとは、一定の時間枠でユーザーが実行できる API リクエストの数を制限する
  - [APIスロットリング制限](https://developer.amazon.com/ja/docs/amazon-pay-api-v2/api-throttling-limits.html)
https://www.django-rest-framework.org/api-guide/throttling/

### ログ設定
https://docs.python.org/ja/3.13/library/logging.handlers.html
- StreamHandler ... ログ出力を sys.stdout, sys.stderr あるいは何らかのファイル風 (file-like) オブジェクト (あるいは、より正確に言えば write() および flush() メソッドをサポートする何らかのオブジェクト) といったストリームに送信する
- FileHandler ... ログ出力をディスク上のファイルに送信する
- RotatingFileHandler ... ディスク上のログファイルに対するローテーション処理をサポートする
- HTTPHandler ... ログ記録メッセージを GET または POST セマンティクスを使って Web サーバに送信する機能をサポートする
- その他いっぱいある
- ログローテーションとは
  - ログファイルが一定のファイルサイズに達したり、一定の期間が経過したらファイル名を変更しログファイルを切り分け、古くなったログファイルは消去する作業を言います。これによって、ログファイルの肥大化を防ぎます。
  - https://linuc.org/study/column/3635/

### その他コマンド

```sh
$ docker compose --env-file ../../.env exec web uv run backend/manage.py migrate
$ docker compose --env-file ../../.env exec web uv run backend/manage.py makemigrations
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose --env-file ../../.env exec web uv run backend/manage.py createsuperuser --noinput

# 環境変数の確認
$ docker compose --env-file ../../.env exec web env
```

### ruff によるコード整形
```sh
$ docker compose --env-file ../../.env exec web uv run ruff check . --fix
$ docker compose --env-file ../../.env exec web uv run ruff format .
```
