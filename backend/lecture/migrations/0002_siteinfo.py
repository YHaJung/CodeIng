# Generated by Django 3.1.1 on 2020-09-13 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Siteinfo',
            fields=[
                ('siteidx', models.AutoField(db_column='siteIdx', primary_key=True, serialize=False)),
                ('sitename', models.CharField(db_column='siteName', max_length=20)),
            ],
            options={
                'db_table': 'siteInfo',
                'managed': False,
            },
        ),
    ]
