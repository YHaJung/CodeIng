# Generated by Django 3.1.1 on 2020-09-21 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20200921_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(2, '2'), (5, '5'), (3, '3'), (1, '1'), (4, '4')], default=None, null=True),
        ),
    ]
