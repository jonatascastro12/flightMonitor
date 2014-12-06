# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20141203_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='destination',
            field=models.CharField(max_length=250),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flight',
            name='origin',
            field=models.CharField(max_length=250),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flight',
            name='searchUrl',
            field=models.CharField(max_length=600),
            preserve_default=True,
        ),
    ]
