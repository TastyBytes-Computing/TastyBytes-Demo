# Generated by Django 4.2.1 on 2024-03-08 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.DateTimeField(blank=True, help_text='The date & time this article was published', null=True),
        ),
    ]
