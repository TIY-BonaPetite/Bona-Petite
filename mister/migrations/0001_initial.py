# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 14:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pH_level', models.FloatField()),
                ('temperature', models.FloatField()),
                ('time_collected', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_Type', models.IntegerField(choices=[(1, 'Commercial'), (2, 'Family'), (3, 'Recreational'), (4, 'Other')])),
                ('crop_Type', models.IntegerField(choices=[(1, 'Flowers'), (2, 'Herbs'), (3, 'Cannabis'), (4, 'Vegetables'), (5, 'Combination')])),
                ('zip_Code', models.FloatField(max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
