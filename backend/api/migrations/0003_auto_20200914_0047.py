# Generated by Django 3.1.1 on 2020-09-13 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200913_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(5, '5'), (3, '3'), (1, '1'), (2, '2'), (4, '4')], default=None, null=True),
        ),
    ]