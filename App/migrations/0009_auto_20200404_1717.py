# Generated by Django 3.0 on 2020-04-05 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_bulkstudent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='class_room',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='parent',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='section',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]