# Generated by Django 2.2.2 on 2019-06-07 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190606_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billentry',
            name='parent',
        ),
    ]
