from blog import signals


def publish_blog(blog_id):
    # Signals を発信するトリガーを定義する
    signals.notify_author.send(sender=None, blog_id=blog_id)
