from rest_framework.versioning import URLPathVersioning


class DefaultDemoAppVersion(URLPathVersioning):
    """demo_app で作成された API のバージョンを管理するためのクラス"""

    allowed_versions = ["v1"]
    version_param = "version"


class DemoViewVersion(DefaultDemoAppVersion):
    """DemoViewで使用するAPIのバージョンを管理するためのクラス"""

    allowed_versions = ["v1", "v2", "v3"]


class AnotherViewVersion(DefaultDemoAppVersion):
    """その他のクラスで使用するAPIのバージョンを管理するためのクラス"""

    allowed_versions = ["v1", "v2"]
