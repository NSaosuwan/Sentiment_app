from django.db import models

# Create your models here.
class Post(models.Model):
    name=models.CharField(max_length=200)
    desc=models.TextField()


class Comment(models.Model):
    Class=models.FloatField()
    Detail=models.TextField()
    Department=models.CharField(max_length=200)
    Aspect=models.CharField(max_length=200)
    words=models.TextField()
    date=models.DateField()