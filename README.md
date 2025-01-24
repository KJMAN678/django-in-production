### Django-in-Production の写経

- [Django-in-Production](https://amzn.asia/d/ev539xN)
- [公式リポジトリ](https://github.com/PacktPublishing/Django-in-Production)

### .env ファイル
- django-in-production ディレクトリ直下に .env ファイルを作成し、下記の環境変数を設定する
```sh
$ touch .env
```
- config/settings.py の SECRET_KEY
SECRET_KEY=""
- createsuperuser 実行時の設定
DJANGO_SUPERUSER_PASSWORD=""
DJANGO_SUPERUSER_USERNAME=""
DJANGO_SUPERUSER_EMAIL=""

### Chapter
- [1章 Django-Rest-Framework](ch01/)
- [2章 Django ORM](ch02/)
