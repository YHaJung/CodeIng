from django.db import models

class Book(models.Model):
    bookidx = models.AutoField(db_column='bookIdx', primary_key=True)  # Field name made lowercase.
    booktitle = models.TextField(db_column='bookTitle')  # Field name made lowercase.
    link = models.TextField()
    thumbnail = models.TextField()
    site = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'book'

