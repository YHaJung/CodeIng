# Generated by Django 3.1.1 on 2020-09-20 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20200920_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(2, '2'), (5, '5'), (3, '3'), (4, '4'), (1, '1')], default=None, null=True),
        ),
    ]