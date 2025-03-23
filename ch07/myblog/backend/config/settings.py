import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "cacheops",
    "debug_toolbar",
]
CUSTOM_APPS = [
    "blog",
    "author",
    "helper",
    "common",
]
INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "common.localthread_middleware.PopulateLocalsThreadMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOSTNAME"),
        "NAME": os.environ.get("POSTGRES_DB_NAME"),
        "USER": os.environ.get("POSTGRES_USERNAME"),
        "PORT": os.environ.get("POSTGRES_PORT"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django Debug Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
RENDER_PANELS = True

# Cache 設定
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://:{os.getenv('REDIS_PASSWORD')}@redis:{os.getenv('REDIS_PORT')}/1",
    }
}

# Cacheops 設定
CACHEOPS_REDIS = {
    "host": "redis",
    "port": os.environ.get("REDIS_PORT"),
    "db": 1,
    "socket_timeout": 3,
    "password": os.environ.get("REDIS_PASSWORD"),
}

# 特定のテーブルのクエリをキャッシュすることができる
# 下記の場合は、auth user テーブルのすべての get クエリをキャッシュする
CACHEOPS = {
    "auth.user": {"ops": "get", "timeout": 60 * 15},
    "auth.*": {"ops": {"fetch", "get"}, "timeout": 60 * 60},
    "blog.blog": {"ops": "all", "timeout": 60 * 60},
}

# スロットリング設定(APIのアクセス制限)
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",  # anon は未認証ユーザーのリクエスト
        "user": "1000/day",  # user は認証ユーザーのリクエスト
        "scope": "10000/day",
        "blog_limit": "1000/day",
    },
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
}

# ロギング設定
LOGGING = {
    # logging.config.dictConfig で設定するための version
    # https://docs.python.org/ja/3.13/library/logging.config.html#logging.config.dictConfig
    "version": 1,
    # デフォルトの Django のロガーを無効化するかどうか
    "disable_existing_loggers": False,
    # logging message のフォーマット
    "formatters": {
        "verbose": {"format": "%(asctime)s %(process)d %(thread)d %(message)s"},
    },
    "loggers": {
        "django_default": {
            # 異なるハンドラーの namespace を設定する事ができる
            "handlers": ["django_file"],
            # ログレベルを設定. DEBUG, INFO, WARNING, ERROR, CRITICAL がある
            "level": "INFO",
        },
    },
    "handlers": {
        # loggers.django_default.handlers で設定したハンドラー名
        "django_file": {
            # ハンドラーのクラスを指定
            "class": "logging.handlers.RotatingFileHandler",
            # ログファイルのパス
            "filename": "logs/django_logs.log",
            # ログファイルの最大サイズ
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            # ローテーションで再利用する前に作成されるバックアップファイルの数
            "backupCount": 10,
            # ログメッセージのフォーマット.
            # verbose ... ログ レベル名、ログ メッセージ、さらにログ メッセージを生成する時間、プロセス、スレッド、モジュールを出力
            # simple ... ログ レベル名、ログ メッセージを出力
            "formatter": "verbose",
        },
    },
}
