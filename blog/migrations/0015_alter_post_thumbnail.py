# Generated by Django 4.2.5 on 2023-11-23 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='blog/static/images/thumbnails/post_default_thumbnail.png', upload_to='blog/static/images/thumbnails/'),
        ),
    ]