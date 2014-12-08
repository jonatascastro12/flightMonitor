# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0009_auto_20141208_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='filteralert',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
