# Generated by Django 4.2.1 on 2023-09-14 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='post',
            new_name='blog_post_publish_bb7600_idx',
            old_name='blog_posts__publish_a7cbc6_idx',
        ),
    ]
