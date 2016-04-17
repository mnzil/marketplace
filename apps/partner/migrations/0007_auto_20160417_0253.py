# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0006_auto_20160417_0250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='shop',
        ),
        migrations.AddField(
            model_name='partner',
            name='shop',
            field=models.ForeignKey(default=1, to='partner.Shop'),
            preserve_default=False,
        ),
    ]
