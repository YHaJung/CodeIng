# Generated by Django 3.1.1 on 2020-09-13 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categoryidx', models.AutoField(db_column='categoryIdx', primary_key=True, serialize=False)),
                ('categoryname', models.CharField(db_column='categoryName', max_length=20)),
            ],
            options={
                'db_table': 'category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('lectureidx', models.AutoField(db_column='lectureIdx', primary_key=True, serialize=False)),
                ('lecturename', models.CharField(db_column='lectureName', max_length=60)),
                ('price', models.CharField(max_length=20)),
                ('lecturelink', models.TextField(db_column='lectureLink')),
                ('thumburl', models.TextField(blank=True, db_column='thumbUrl', null=True)),
                ('level', models.DecimalField(decimal_places=3, max_digits=4)),
                ('lecturer', models.CharField(blank=True, max_length=300, null=True)),
                ('siteidx', models.IntegerField(db_column='siteIdx')),
                ('rating', models.DecimalField(decimal_places=3, max_digits=4)),
                ('createdat', models.DateTimeField(db_column='createdAt')),
                ('updatedat', models.DateTimeField(blank=True, db_column='updatedAt', null=True)),
                ('isdeleted', models.CharField(db_column='isDeleted', max_length=1)),
            ],
            options={
                'db_table': 'lecture',
                'managed': False,
            },
        ),
    ]
