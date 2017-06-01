# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('foodspark', '0014_order_orderdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='foodlist',
            field=models.CharField(max_length=500, null=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\d,]+\\Z'), 'Enter only digits separated by commas.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='foodqty',
            field=models.CharField(max_length=500, null=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\d,]+\\Z'), 'Enter only digits separated by commas.', 'invalid')]),
        ),
    ]
