# Generated by Django 3.0 on 2020-04-04 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_auto_20200403_2201'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulkStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('parent', models.CharField(max_length=100)),
                ('class_room', models.CharField(max_length=100)),
                ('session', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.TextField()),
            ],
        ),
    ]
