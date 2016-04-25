# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0007_auto_20160417_0253'),
        ('offer', '0003_range_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='conditionaloffer',
            name='shop',
            field=models.ForeignKey(default=1, to='partner.Shop'),
            preserve_default=False,
        ),
    ]
