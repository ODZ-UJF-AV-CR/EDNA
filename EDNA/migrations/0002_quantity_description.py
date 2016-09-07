# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EDNA', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantity',
            name='description',
            field=models.TextField(default='kecy prdy recicky'),
            preserve_default=False,
        ),
    ]
