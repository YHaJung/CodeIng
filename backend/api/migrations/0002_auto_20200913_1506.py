# Generated by Django 3.1.1 on 2020-09-13 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(2, '2'), (1, '1'), (5, '5'), (3, '3'), (4, '4')], default=None, null=True),
        ),
    ]
