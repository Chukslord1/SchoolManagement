# Generated by Django 3.0 on 2020-04-10 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_auto_20200409_0417'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]
