# Generated by Django 3.0 on 2020-04-23 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0019_userprofile_qr_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.FileField(upload_to='media/'),
        ),
    ]
