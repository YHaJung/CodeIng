# Generated by Django 3.1.1 on 2020-09-15 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20200915_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(4, '4'), (2, '2'), (5, '5'), (3, '3'), (1, '1')], default=None, null=True),
        ),
    ]
