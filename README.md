### Django-in-Production の写経

- [Django-in-Production](https://amzn.asia/d/ev539xN)
- [公式リポジトリ](https://github.com/PacktPublishing/Django-in-Production)

### .env ファイル
- django-in-production ディレクトリ直下に .env ファイルを作成し、下記の環境変数を設定する
```sh
$ touch .env
```
- config/settings.py の SECRET_KEY
```sh
SECRET_KEY=""
```
- createsuperuser 実行時の設定
```sh
DJANGO_SUPERUSER_PASSWORD=""
DJANGO_SUPERUSER_USERNAME=""
DJANGO_SUPERUSER_EMAIL=""
```

### Chapter
- [1章 Django-Rest-Framework](ch01/)
- [2章 Django ORM](ch02/)
- [3章 DRF による データ Serialize 処理](ch03/)
- [4章 Django Admin, Management Command](ch04/)
- [5章 認証認可](ch05/)
- [(未了) 6章 キャッシュ, ログ, スロットリング]
- [(未了) 7章 ページネーション, Django シグナル, カスタムミドルウェア]
- [(未了) 8章 Celery による非同期処理]
- [(未了) 9章 テスト]
- [(未了) 10章 Django の慣例]
- [(未了) 11章 Docker]
- [(未了) 12章 Git, CI]
- [(未了) 13章 AWS にデプロイ by AppRouter]
- [(未了) 14章 監視]
