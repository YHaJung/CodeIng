from django.db import models

class Siteinfo(models.Model):
    siteidx = models.AutoField(primary_key=True)  # Field name made lowercase.
    sitename = models.CharField(max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'siteInfo'




class Lecture(models.Model):
        lectureidx = models.AutoField(db_column='lectureIdx', primary_key=True)  # Field name made lowercase.
        lecturename = models.CharField(db_column='lectureName', max_length=60)  # Field name made lowercase.
        price = models.CharField(max_length=20)
        lecturelink = models.TextField(db_column='lectureLink')  # Field name made lowercase.
        thumburl = models.TextField(db_column='thumbUrl', blank=True, null=True)  # Field name made lowercase.
        level = models.DecimalField(max_digits=4, decimal_places=3)
        lecturer = models.CharField(max_length=300, blank=True, null=True)
        rating = models.DecimalField(max_digits=4, decimal_places=3)
        createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
        updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
        isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

        siteinfo = models.ForeignKey(Siteinfo, on_delete=models.CASCADE,
                                    db_column='siteidx')  # Field name made lowercase.

        class Meta:
            managed = False
            db_table = 'lecture'





class Category(models.Model):
    categoryidx = models.AutoField(db_column='categoryIdx', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='categoryName', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'category'
