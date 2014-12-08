# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20141204_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='destination',
            field=models.CharField(max_length=250, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flight',
            name='price',
            field=models.DecimalField(max_digits=6, decimal_places=2, db_index=True),
            preserve_default=True,
        ),
    ]
