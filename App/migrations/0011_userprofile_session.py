# Generated by Django 3.0 on 2020-04-07 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_auto_20200407_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='session',
            field=models.CharField(default='2020 - 2021', max_length=100),
            preserve_default=False,
        ),
    ]
