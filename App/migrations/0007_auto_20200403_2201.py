# Generated by Django 3.0 on 2020-04-04 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_auto_20200403_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='secret_pin',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]