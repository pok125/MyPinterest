# Generated by Django 4.2.1 on 2023-07-24 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_followrecord'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followrecord',
            unique_together={('following_user', 'followed_user')},
        ),
    ]