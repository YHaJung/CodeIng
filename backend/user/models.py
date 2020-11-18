from django.db import models

# Create your models here.

class Level(models.Model):
    levelidx = models.AutoField(db_column='levelIdx', primary_key=True)  # Field name made lowercase.
    levelname = models.CharField(db_column='levelName', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'level'

class Userinfo(models.Model):
    useridx = models.AutoField(db_column='userIdx', primary_key=True)  # Field name made lowercase.
    profileimg = models.CharField(db_column='profileImg', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    nickname = models.CharField(db_column='nickName', max_length=45)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt',auto_now=True, blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userInfo'


class Profile(models.Model):
    userinfo = models.OneToOneField(Userinfo, on_delete=models.CASCADE, db_column='userIdx', primary_key=True)
    userpwd = models.CharField(db_column='userPwd', max_length=200)  # Field name made lowercase.
    gender = models.CharField(max_length=1)
    name = models.CharField(max_length=45)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=20)  # Field name made lowercase.
    school = models.CharField(max_length=30, blank=True, null=True)
    job = models.CharField(max_length=1, blank=True, null=True)
    isblocked = models.CharField(db_column='isBlocked', max_length=1)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt',auto_now=True, blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True, db_column='level')

    class Meta:
        managed = False
        db_table = 'profile'


class Category(models.Model):
    categoryidx = models.AutoField(db_column='categoryIdx', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='categoryName', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'category'


class Subcategory(models.Model):
    subcategoryidx = models.AutoField(db_column='subCategoryIdx', primary_key=True)  # Field name made lowercase.
    subcategoryname = models.CharField(db_column='subCategoryName', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subCategory'

class Categoryinterest(models.Model):
    categoryinterestidx = models.AutoField(db_column='categoryInterestIdx',
                                           primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt',auto_now=True, blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.
    useridx = models.ForeignKey(Userinfo, on_delete=models.CASCADE, db_column='userIdx')  # Field name made lowercase.
    categoryidx = models.ForeignKey(Category, on_delete=models.CASCADE,
                                      db_column='categoryIdx')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoryInterest'


class Subcategoryinterest(models.Model):
    subcategoryinterestidx = models.AutoField(db_column='subCategoryInterestIdx',
                                              primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt',auto_now=True, blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    useridx = models.ForeignKey(Userinfo, on_delete=models.CASCADE, db_column='userIdx')  # Field name made lowercase.
    subcategoryidx = models.ForeignKey(Subcategory, on_delete=models.CASCADE,
                                         db_column='subcategoryIdx')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subCategoryInterest'
