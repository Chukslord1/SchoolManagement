# Generated by Django 3.0 on 2020-04-23 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0022_facereg_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facereg',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]