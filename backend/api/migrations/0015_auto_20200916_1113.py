# Generated by Django 3.1.1 on 2020-09-16 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20200915_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, choices=[(1, '1'), (4, '4'), (2, '2'), (3, '3'), (5, '5')], default=None, null=True),
        ),
    ]
