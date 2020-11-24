from django.db import models


class Siteinfo(models.Model):
    siteidx = models.AutoField(primary_key=True)  # Field name made lowercase.
    sitename = models.CharField(max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'siteInfo'




class Userinfo(models.Model):
    useridx = models.AutoField(db_column='userIdx', primary_key=True)  # Field name made lowercase.
    profileimg = models.CharField(db_column='profileImg', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    nickname = models.CharField(db_column='nickName', max_length=45)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userInfo'




class Level(models.Model):
    levelidx = models.AutoField(db_column='levelIdx', primary_key=True)  # Field name made lowercase.
    levelname = models.CharField(db_column='levelName', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'level'




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
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True, db_column='level')

    class Meta:
        managed = False
        db_table = 'profile'


class Lecture(models.Model):
    lectureidx = models.AutoField(db_column='lectureIdx', primary_key=True)  # Field name made lowercase.
    lecturename = models.CharField(db_column='lectureName', max_length=60)  # Field name made lowercase.
    price = models.IntegerField(blank=True, null=True)
    lecturelink = models.TextField(db_column='lectureLink')  # Field name made lowercase.
    thumburl = models.TextField(db_column='thumbUrl', blank=True, null=True)  # Field name made lowercase.

    lecturer = models.CharField(max_length=300, blank=True, null=True)
    rating = models.DecimalField(max_digits=4, decimal_places=3)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    siteinfo = models.ForeignKey(Siteinfo, on_delete=models.CASCADE,
                                 db_column='siteidx')  # Field name made lowercase.

    #level = models.IntegerField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE, db_column='level')


    class Meta:
        managed = False
        db_table = 'lecture'



class Choice(models.Model):
    choiceidx = models.AutoField(db_column='choiceIdx', primary_key=True)  # Field name made lowercase.
    content = models.TextField()
    quizidx = models.IntegerField(db_column='quizIdx')  # Field name made lowercase.
    choicenum = models.IntegerField(db_column='choiceNum')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'choice'




class Study(models.Model):
    classidx = models.AutoField(db_column='classIdx', primary_key=True)  # Field name made lowercase.
    classname = models.CharField(db_column='className', max_length=100)  # Field name made lowercase.
    password = models.CharField(max_length=100, blank=True, null=True)

    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    lectureidx = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_column='lectureIdx')



    leaderidx = models.ForeignKey(Userinfo, on_delete=models.CASCADE,
                                 db_column='leaderIdx')  # Field name made lowercase.



    class Meta:
        managed = False
        db_table = 'study'



class Classmember(models.Model):
    classmemberidx = models.AutoField(db_column='classmemberIdx', primary_key=True)  # Field name made lowercase.
    classidx = models.ForeignKey(Study, on_delete=models.CASCADE, db_column='classIdx')
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE, db_column='userIdx')  # Field name made lowercase.
    progress = models.IntegerField()
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'classMember'


class Classtag(models.Model):
    classtagidx = models.AutoField(db_column='classTagIdx', primary_key=True)  # Field name made lowercase.
    classidx = models.ForeignKey(Study, on_delete=models.CASCADE, db_column='classIdx')
    tagname = models.CharField(db_column='tagName', max_length=20)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.CharField(db_column='isDeleted', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'classTag'



