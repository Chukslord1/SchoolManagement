# Generated by Django 3.0 on 2020-03-21 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_auto_20200321_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unusedpins',
            name='user',
        ),
    ]