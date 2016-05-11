# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import oscar.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('partner', '0008_auto_20160506_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.SmallIntegerField(verbose_name='Score', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('title', models.CharField(max_length=255, verbose_name='Title', validators=[oscar.core.validators.non_whitespace])),
                ('body', models.TextField(verbose_name='Body')),
                ('name', models.CharField(max_length=255, verbose_name='Name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email', blank=True)),
                ('homepage', models.URLField(verbose_name='URL', blank=True)),
                ('status', models.SmallIntegerField(default=1, verbose_name='Status', choices=[(0, 'Requires moderation'), (1, 'Approved'), (2, 'Rejected')])),
                ('total_votes', models.IntegerField(default=0, verbose_name='Total Votes')),
                ('delta_votes', models.IntegerField(default=0, verbose_name='Delta Votes', db_index=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(related_name='shopreviews', on_delete=django.db.models.deletion.SET_NULL, to='partner.Shop', null=True)),
                ('user', models.ForeignKey(related_name='shopreviews', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-delta_votes', 'id'],
                'verbose_name': 'Shop review',
                'verbose_name_plural': 'Shop reviews',
            },
        ),
        migrations.AlterUniqueTogether(
            name='shopreview',
            unique_together=set([('shop', 'user')]),
        ),
    ]
