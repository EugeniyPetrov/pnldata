# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-07 16:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pnldata', '0008_auto_20170307_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='purse_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='expenseset',
            name='tag1',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags1', to='pnldata.Tag'),
        ),
        migrations.AlterField(
            model_name='expenseset',
            name='tag2',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags2', to='pnldata.Tag'),
        ),
        migrations.AlterField(
            model_name='expenseset',
            name='tag3',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='tags3', to='pnldata.Tag'),
        ),
    ]
