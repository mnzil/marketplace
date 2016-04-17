# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0006_auto_20160417_0250'),
        ('catalogue', '0009_productclass_partner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productclass',
            name='partner',
        ),
        migrations.AddField(
            model_name='productclass',
            name='shop',
            field=models.OneToOneField(default=1, to='partner.Shop'),
            preserve_default=False,
        ),
    ]
