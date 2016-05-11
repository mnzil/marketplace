# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0007_auto_20160417_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='image',
            field=models.ImageField(upload_to=b'images/products/%Y/%m/', max_length=255, verbose_name=b'image', blank=True),
        ),
    ]
