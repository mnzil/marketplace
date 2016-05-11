# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopreviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delta', models.SmallIntegerField(verbose_name='Delta', choices=[(1, 'Up'), (-1, 'Down')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(related_name='votes', to='shopreviews.ShopReview')),
                ('user', models.ForeignKey(related_name='shopreview_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_created'],
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
            },
        ),
        migrations.AlterUniqueTogether(
            name='shopvote',
            unique_together=set([('user', 'review')]),
        ),
    ]
