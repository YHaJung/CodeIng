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
    price = models.IntegerField(blank=True, null=True)
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


class Subcategory(models.Model):
    subcategoryidx = models.AutoField(db_column='subCategoryIdx', primary_key=True)  # Field name made lowercase.
    subcategoryname = models.CharField(db_column='subCategoryName', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'subCategory'


class Lecturecategory(models.Model):

    categoryidx = models.IntegerField(db_column='categoryIdx')  # Field name made lowercase.
    lecturecategoryidx = models.AutoField(db_column='lectureCategoryIdx', primary_key=True)  # Field name made lowercase.

    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE, db_column='subCategoryIdx')  # Field name made lowercase.
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_column='lectureIdx')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'lectureCategory'


class Level(models.Model):
    levelidx = models.AutoField(db_column='levelIdx', primary_key=True)  # Field name made lowercase.
    levelname = models.CharField(db_column='levelName', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'level'


class Userinfo(models.Model):
    useridx = models.AutoField(db_column='userIdx', primary_key=True)  # Field name made lowercase.
    profileimg = models.CharField(db_column='profileImg', max_length=45, blank=True, null=True)  # Field name made lowercase.
    nickname = models.CharField(db_column='nickName', max_length=45)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'userInfo'


class Profile(models.Model):
    userinfo = models.OneToOneField(Userinfo, on_delete=models.CASCADE, db_column='userIdx', primary_key=True)
    userid = models.CharField(db_column='userId', max_length=45)  # Field name made lowercase.
    userpwd = models.CharField(db_column='userPwd', max_length=45)  # Field name made lowercase.
    gender = models.CharField(max_length=1)
    name = models.CharField(max_length=45)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    phonenumber = models.CharField(db_column='phoneNumber', max_length=20)  # Field name made lowercase.
    school = models.CharField(max_length=30, blank=True, null=True)
    job = models.CharField(max_length=1, blank=True, null=True)
    major = models.CharField(max_length=1, blank=True, null=True)
    isblocked = models.CharField(db_column='isBlocked', max_length=1)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True, db_column='level')


    class Meta:
        managed = False
        db_table = 'profile'


class Review(models.Model):
    reviewidx = models.AutoField(db_column='reviewIdx', primary_key=True)  # Field name made lowercase.
    lectureidx = models.IntegerField(db_column='lectureIdx')  # Field name made lowercase.
    totalrating = models.DecimalField(db_column='totalRating', max_digits=2, decimal_places=1)  # Field name made lowercase.
    pricerating = models.DecimalField(db_column='priceRating', max_digits=2, decimal_places=1)  # Field name made lowercase.
    teachingpowerrating = models.DecimalField(db_column='teachingPowerRating', max_digits=2, decimal_places=1)  # Field name made lowercase.
    recommend = models.CharField(max_length=1)
    isblocked = models.CharField(db_column='isBlocked', max_length=1)  # Field name made lowercase.
    improvement = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='userIdx')  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'review'

class Cons(models.Model):
    considx = models.AutoField(db_column='consIdx', primary_key=True)  # Field name made lowercase.
    constype = models.CharField(db_column='consType', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cons'

class Pros(models.Model):
    prosidx = models.AutoField(db_column='prosIdx', primary_key=True)  # Field name made lowercase.
    prostype = models.CharField(db_column='prosType', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pros'


class Reviewcons(models.Model):
    reviewconsidx = models.AutoField(db_column='reviewConsIdx', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    review = models.ForeignKey(Review, on_delete=models.CASCADE, db_column='reviewIdx')  # Field name made lowercase.
    cons = models.ForeignKey(Cons, on_delete=models.CASCADE, db_column='consIdx')


    class Meta:
        managed = False
        db_table = 'reviewCons'


class Reviewpros(models.Model):
    reviewprosidx = models.AutoField(db_column='reviewProsIdx', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    review = models.ForeignKey(Review, on_delete=models.CASCADE, db_column='reviewIdx')
    pros = models.ForeignKey(Pros, on_delete=models.CASCADE, db_column='prosIdx')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reviewPros'



class Likesforqna(models.Model):
    likesforqnaidx = models.AutoField(db_column='likesForQnAIdx', primary_key=True)  # Field name made lowercase.
    useridx = models.IntegerField(db_column='userIdx')  # Field name made lowercase.
    qnaidx = models.IntegerField(db_column='qnaIdx')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'likesForQnA'


class Likesforreview(models.Model):
    likesforreview = models.AutoField(db_column='likesForReview', primary_key=True)  # Field name made lowercase.
    useridx = models.IntegerField(db_column='userIdx')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    review = models.ForeignKey(Review, on_delete=models.CASCADE, db_column='reviewIdx')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'likesForReview'

