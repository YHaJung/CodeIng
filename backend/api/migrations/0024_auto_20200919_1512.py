# Generated by Django 3.1.1 on 2020-09-19 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20200919_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(5, '5'), (3, '3'), (1, '1'), (2, '2'), (4, '4')], default=None, null=True),
        ),
    ]