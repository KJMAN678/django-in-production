# Generated by Django 5.1.5 on 2025-01-23 10:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("author", "0002_author_created_at_author_updated_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogAuthor",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("author.author",),
        ),
        migrations.AddField(
            model_name="author",
            name="demo_field",
            field=models.TextField(default="demo"),
        ),
    ]
