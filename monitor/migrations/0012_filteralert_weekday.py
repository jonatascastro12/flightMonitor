# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0011_auto_20141208_0904'),
    ]

    operations = [
        migrations.AddField(
            model_name='filteralert',
            name='weekday',
            field=models.PositiveIntegerField(default=128, choices=[(1, b'Segunda'), (2, b'Ter\xc3\xa7a'), (4, b'Quarta'), (8, b'Quinta'), (16, b'Sexta'), (32, b'S\xc3\xa1bado'), (64, b'Domingo')]),
            preserve_default=True,
        ),
    ]
