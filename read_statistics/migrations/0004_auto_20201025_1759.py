# Generated by Django 2.2 on 2020-10-25 17:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0003_auto_20201025_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 25, 17, 59, 6, 250420)),
        ),
    ]
