# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-06 11:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Advocate', '0023_auto_20160906_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='advocate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Advocate.SiteUser'),
        ),
    ]