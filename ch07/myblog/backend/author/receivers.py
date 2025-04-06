from django.dispatch import receiver
from blog import signals


@receiver(signals.notify_author)
def send_email_to_author(sender, blog_id, **kwargs):
    # author に メールを送信する
    print("sending email to author logic", blog_id)
