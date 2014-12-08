# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0007_filteralert'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filteralert',
            old_name='price',
            new_name='maxPrice',
        ),
    ]
