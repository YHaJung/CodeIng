# Generated by Django 3.1.1 on 2020-09-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20200919_0118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(5, '5'), (2, '2'), (1, '1'), (4, '4'), (3, '3')], default=None, null=True),
        ),
    ]
