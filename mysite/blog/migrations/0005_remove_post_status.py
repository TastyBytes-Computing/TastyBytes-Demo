# Generated by Django 4.2.1 on 2024-02-24 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
    ]
