# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0010_filteralert_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filteralert',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
