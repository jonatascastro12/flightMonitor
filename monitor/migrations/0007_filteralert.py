# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20141207_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('destinationFilter', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=75)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('dateStart', models.DateField()),
                ('dateEnd', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
