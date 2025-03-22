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
http://127.0.0.1:8000/blog/blogs_auto_invalidation/?author_id=1
http://127.0.0.1:8000/blog/blogs_anon_view/
http://127.0.0.1:8000/blog/blogs_user_view/
http://127.0.0.1:8000/blog/blogs_scoped_view/

- def log_event() でログを記録する
http://127.0.0.1:8000/blog/blogs_logs/?author_id=1

http://127.0.0.1:8000/admin/login/

- スレッドローカルストレージ（Thread Local Storage、TLS）
  - マルチスレッドプログラムにおいて、各スレッドが独自のデータを保持するためのメモリ領域を指す
  - [参考](https://www.notion.so/1be29a2fd70e804489b4d168455c3f64)

# ログ解析ツール

- New Relic
  - New Relicは、アプリケーションパフォーマンス監視（APM）を中心としたフルスタックのオブザーバビリティプラットフォームです。
  - ​アプリケーションのレスポンスタイム、エラー率、トランザクションなどの指標をリアルタイムでモニタリングし、問題の早期検出と迅速な対応を支援します。​
  - 特に、コードレベルでの詳細な可視化が可能であり、異常の根本原因分析を容易にします。​また、ダッシュボード機能により、チーム内での情報共有や意思決定の迅速化にも寄与します。

- Elasticsearch-Logstash-Kibana（ELK）スタック
  - ELKスタックは、以下の3つの主要コンポーネントから構成されるオープンソースのログ管理および分析プラットフォームです。

- Sentry
  - リアルタイムのエラートラッキングツールで、Djangoとの統合が容易です。
  - エラーの発生状況を即座に把握し、迅速な対応が可能となります。 ​

- Django Debug Toolbar
  - 開発中のデバッグを支援するツールで、SQLクエリの詳細やテンプレートのレンダリング時間など、詳細な情報を提供します。 ​

- Django Extensions
  - 追加の管理コマンドやツールを提供するパッケージで、開発やデバッグの効率化に役立ちます。 ​

- Splunk
  - 大規模なデータ分析プラットフォームで、ログの収集、検索、分析を強力にサポートします。​

- Graylog
  - オープンソースのログ管理ツールで、リアルタイムのログ解析やアラート機能を備えています。

# 本番環境でのログのベストプラクティス

- 本番環境でエラーを収集するためにログ記録を使用してはならない
  - 小規模なプロジェクトでは通用するが、大規模になるとつらみが増す
  - [Sentry](https://sentry.io/welcome/) や [Rollbar](https://rollbar.com/platforms/python-error-tracking/) を使うと良い

- ログの転送にメールを使用してはならない
  - ログ管理エージェントを利用すると良い
  - [New Relic](https://docs.newrelic.com/jp/docs/apm/agents/python-agent/getting-started/introduction-new-relic-python/) や [Elasticsearch-Logstash-Kibana（ELK）スタック](https://www.elastic.co/elastic-stack) など

- 機密情報をログに流してはならない
  - 例
    - メールアドレス
    - パスワード
    - 支払いの詳細

- 共通のログ機能を使用すること。
  - これにより、ログの形式が統一される
  - ログエージェントによる解析が容易になる
  - ログの解析がやりやすくなる

- 現在のユースケースが終了したら、ログを削除すること.
  - 古いログや不要なログを残し続けると、コストがかかってしまう
  - アプリケーションが大きくなったら、古いロギング関数の呼び出しを削除したという経過を追った方が良い.

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
