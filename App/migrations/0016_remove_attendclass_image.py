# Generated by Django 3.0 on 2020-04-11 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0015_auto_20200410_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendclass',
            name='image',
        ),
    ]
