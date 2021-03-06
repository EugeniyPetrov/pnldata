# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-07 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pnldata', '0005_remove_expense_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='expenseset',
            name='description',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='expenseset',
            name='tag1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tags1', to='pnldata.Tag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expenseset',
            name='tag2',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tags2', to='pnldata.Tag'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expenseset',
            name='tag3',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tags3', to='pnldata.Tag'),
            preserve_default=False,
        ),
    ]
