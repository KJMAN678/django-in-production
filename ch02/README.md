```sh
# 初回のみ ディレクトリ作成、プロジェクト作成
$ cd ch02/myblog
$ uv run django-admin startproject config backend/

# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env up --detach
# Docker再ビルド
$ docker compose --env-file ../../.env build

$ docker compose exec web uv run backend/manage.py migrate
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose exec web uv run backend/manage.py createsuperuser --noinput
```

http://localhost:8000/
http://localhost:8000/admin/login/
http://localhost:8000/blog/async_get_blog/
http://localhost:8000/blog/get_blog/

### 公開されるサービスでは psycopg2-binary は使わないこと
https://www.psycopg.org/docs/install.html#psycopg-vs-psycopg-binary

```sh
$ mkdir backend/author
$ docker compose exec web uv run django-admin startapp author backend/author
$ mkdir backend/blog
$ docker compose exec web uv run django-admin startapp blog backend/blog
```

### model メモ
- blank=True/False はアプリケーション上の制約
- null=True/False はデータベース上の制約

### ダミーデータ登録
```sh
$ mkdir backend/helper
$ docker compose exec web uv run django-admin startapp helper backend/helper

$ docker compose exec web uv run backend/manage.py create_dummy_data

$ docker compose exec web uv run backend/manage.py done_query
```

### SQLで確認
- hostname は 127.0.0.1
- port は Dockerが指定している方 5432:5432 の前の方の 5432
```sql
# テーブル一覧
select schemaname, tablename, tableowner from pg_tables;

# データ取得
select * from blog_blog;
select * from author_author;
```

### ManyToManyModel で中間テーブルを指定する
https://docs.djangoproject.com/en/5.1/ref/models/fields/#django.db.models.ManyToManyField.through
https://qiita.com/mkizka/items/da4f8031d44fe1cdf353

### Proxy Model
https://docs.djangoproject.com/ja/5.1/topics/db/models/#proxy-models
https://tokibito.hatenablog.com/entry/2017/12/07/235805

### fake migration
```sh
$ docker compose exec web uv run backend/manage.py migrate author 0002 --fake
```

### TIMEZONE
https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/

### Circular Dependency in models.py

- ForeignKeyの中身を文字列に変換すれば循環参照を回避できる

### Model Manager
https://docs.djangoproject.com/en/5.1/topics/db/managers/
- カスタムマネージャーを利用すると、複数のmodelで再利用できる共通のクエリロジックを作ることができる
- 下記の例では、Article.published.all() を呼び出すと、is_published=True の記事だけを取得できる
```python
from django.db import models

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)

    # カスタムマネージャーを設定
    objects = models.Manager()  # デフォルトマネージャー
    published = PublishedManager()  # カスタムマネージャー
```
- カスタムメソッドを追加できる
- 下記の例では Article.objects.recent_articles() で新着10件記事を表示できる
```python
    def recent_articles(self):
        return self.get_queryset().order_by('-created_at')[:10]

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ArticleManager()
```

### UUID
https://docs.djangoproject.com/ja/5.1/ref/models/fields/#uuidfield

### トランザクション
https://docs.djangoproject.com/en/5.1/topics/db/transactions/

### 状態管理用のライブラリ (Finite State Machine)
https://github.com/django-commons/django-fsm-2

### models.py の中身を分割する
https://docs.djangoproject.com/en/5.1/topics/db/models/#organizing-models-in-a-package

-- models  
  |- `__init__`.py  
  |- hoge.py  
  |- fuga.py  

- __init__.py で各ファイルをimport する
```python
from .hoge import Hoge
from .fuga import Fuga
```

### PostgreSQL の EXPLAIN 機能
https://www.postgresql.org/docs/current/sql-explain.html

- PostgreSQLのEXPLAINプラン解析は、データベースクエリの実行計画（Execution Plan）を理解し、性能を最適化するためのプロセスです。これにより、クエリがどのように実行されるかを詳しく確認でき、ボトルネックや改善の余地を特定できます。

- EXPLAINとは？
  - EXPLAINコマンドを使うことで、PostgreSQLはクエリ実行時に使用するプランを表示します。このプランには、テーブルスキャン、インデックスの使用、結合アルゴリズム、並列処理などの情報が含まれています。

- EXPLAIN ANALYZEは、実際にクエリを実行した結果とともに、実行プランを表示します。これにより、理論的なプランと実際の実行結果を比較できます。

- ノードタイプ（Node Type）
  - クエリの各ステップを表す部分（例：Seq Scan、Index Scan、Nested Loopなど）。
  - これにより、どのようにデータがスキャンまたは結合されるかが分かります。

- コスト（cost=）
  - PostgreSQLの内部的なコスト推定値（開始コストと終了コスト）。
  - cost=0.00..35.50 は、開始コストが0、終了コストが35.50を意味します。

- 推定行数と幅（rows=, width=）
  - rows=10 は、このステップで処理される行数の推定値。
  - width=4 は、1行の平均サイズ（バイト単位）。
  - 実行時間（actual time=）
  - actual time=0.025..0.045 は、ステップの開始から終了までの実際の時間（ミリ秒）。

- ループ数（loops=）
  - ステップが実行された回数。結合やネストされた操作で特に重要。

- フィルタ条件（Filter:）
  - データがどの条件でフィルタリングされているかを示します。

- プランニングと実行時間
  - Planning Time はクエリプランの作成時間。
  - Execution Time はクエリ全体の実行時間。

### Exists VS Count
- データが存在するか確かめたいときは、データが大きい場合は、len(query) < count() < exits() でパフォーマンスがよい.

### select_related, prefetch_related

- select_related
  - 外部キーや一対一（OneToOne）リレーションを使用する場合に、関連するオブジェクトをSQLのJOINを使って一度のクエリで取得します。

- prefetch_related
  - 多対多（ManyToMany）や逆方向の多対一（ForeignKeyの逆方向）の関連データを効率的に取得する際に使います。
  - 複数のクエリを実行し、Python 側で関連付けを行う

### bulk_create は注意点がある
https://docs.djangoproject.com/en/5.1/ref/models/querysets/#bulk-create

1. save() メソッドが呼び出されず、pre_save と post_save シグナルが送信されない
- 通常、モデルインスタンスを保存するときには、その save() メソッドが実行され、カスタムロジックを追加することができます。しかし、bulk_create ではパフォーマンス向上のために直接データベースに挿入されるため、save() メソッドは実行されません。
- さらに、Django のシグナルである pre_save と post_save も呼び出されません。これにより、通常の保存処理時にトリガーされる追加の処理が実行されない点に注意が必要です。

2. マルチテーブル継承での子モデルには対応していない
- Django のマルチテーブル継承（モデル継承）を使っている場合、親モデルと子モデルにそれぞれデータが保存されます。しかし、bulk_create はこの構造をサポートしておらず、子モデルのオブジェクトを保存しようとするとエラーが発生する可能性があります。
- このため、マルチテーブル継承を使用する場合は、個別に保存処理を行う必要があります。

3. AutoField の主キーと ignore_conflicts=False の制約
- モデルの主キーが AutoField（自動採番）である場合、bulk_create 実行後に主キーの値を取得できるかどうかはデータベースによって異なります。
- PostgreSQL、MariaDB、SQLite 3.35+ では主キーが適切に設定されますが、それ以外のデータベースでは主キーの値は設定されません。
- これを避けたい場合は、これらのデータベースを使用するか、別の方法で主キーを管理する必要があります。

4. 多対多（Many-to-Many）関係には対応していない
- Django の多対多フィールドは中間テーブルを通じて関係を管理します。しかし、bulk_create は直接データベースに挿入するため、この中間テーブルを適切に扱うことができません。
- 多対多フィールドを設定する場合は、オブジェクトを保存した後に add() メソッドなどで関係を設定する必要があります。

5. objs をリストにキャストする
- bulk_create は内部で objs（挿入するオブジェクトのリスト）をリストにキャストします。このとき、objs がジェネレータである場合には、ジェネレータがすべて評価されます。
- これは、手動で主キーを設定したオブジェクトを先に挿入する必要がある場合に問題を回避するためですが、大量のデータを扱うときにメモリ使用量が増える可能性があります。

6. バッチ処理での注意点
- 大量のデータを挿入する場合、bulk_create を小さなバッチに分割して処理することでメモリの使用量を抑えることができます。
ただし、オブジェクトに手動で設定された主キーが含まれる場合、この方法は使用できません。

### get_or_create and update_or_create
https://docs.djangoproject.com/en/5.1/ref/models/querysets/#get-or-create
- リクエストが並行して行われたときに重複したオブジェクトが作成されるのを防げる

### DB 設定
https://docs.djangoproject.com/en/5.1/ref/databases/#persistent-connections
- CONN_MAX_AGE ... 接続を継続できる秒数

### Asynchronous-Queries
https://docs.djangoproject.com/en/5.1/topics/db/queries/#asynchronous-queries

### Transaction
https://docs.djangoproject.com/en/5.1/topics/db/queries/#transactions

### その他コマンド

```sh
$ docker compose exec web uv run backend/manage.py migrate
$ docker compose exec web uv run backend/manage.py makemigrations
$ docker compose exec web uv run backend/manage.py createsuperuser

# 環境変数の確認
$ docker compose exec web env
$ docker compose --env-file ../../.env exec web env
```

### ruff によるコード整形
```sh
$ docker compose exec web uv run ruff check . --fix
$ docker compose exec web uv run ruff format .
```
