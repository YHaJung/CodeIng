# Generated by Django 3.1.1 on 2020-09-15 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200914_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(5, '5'), (4, '4'), (3, '3'), (1, '1'), (2, '2')], default=None, null=True),
        ),
    ]
