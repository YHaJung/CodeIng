# Generated by Django 3.1.1 on 2020-09-19 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20200919_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(1, '1'), (2, '2'), (4, '4'), (3, '3'), (5, '5')], default=None, null=True),
        ),
    ]
