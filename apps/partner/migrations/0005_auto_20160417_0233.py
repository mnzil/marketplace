# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import oscar.models.fields.autoslugfield


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_auto_20160107_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', oscar.models.fields.autoslugfield.AutoSlugField(populate_from=b'name', editable=False, max_length=128, blank=True, unique=True, verbose_name='Code')),
                ('title', models.CharField(max_length=128, verbose_name='Name', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='partner',
            name='shop',
            field=models.ManyToManyField(to='partner.Shop'),
        ),
    ]
