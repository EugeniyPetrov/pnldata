# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-07 15:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pnldata', '0002_entry'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Entry',
            new_name='Expense',
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={},
        ),
    ]
