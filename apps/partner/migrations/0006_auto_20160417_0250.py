# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import oscar.models.fields.autoslugfield


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0005_auto_20160417_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='code',
            field=oscar.models.fields.autoslugfield.AutoSlugField(populate_from=b'title', editable=False, max_length=128, blank=True, unique=True, verbose_name='Code'),
        ),
    ]
