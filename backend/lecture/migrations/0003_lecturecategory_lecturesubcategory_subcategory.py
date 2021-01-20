# Generated by Django 3.1.1 on 2020-09-16 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0002_siteinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturecategory',
            fields=[
                ('categoryidx', models.IntegerField(db_column='categoryIdx')),
                ('lecturecategoryidx', models.AutoField(db_column='lectureCategoryIdx', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'lectureCategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Lecturesubcategory',
            fields=[
                ('lecturesubcategoryidx', models.AutoField(db_column='lectureSubcategoryIdx', primary_key=True, serialize=False)),
                ('subcategoryidx', models.IntegerField(db_column='subCategoryIdx')),
            ],
            options={
                'db_table': 'lectureSubCategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('subcategoryidx', models.AutoField(db_column='subCategoryIdx', primary_key=True, serialize=False)),
                ('subcategoryname', models.CharField(db_column='subCategoryName', max_length=20)),
            ],
            options={
                'db_table': 'subCategory',
                'managed': False,
            },
        ),
    ]
