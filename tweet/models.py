from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    username = models.CharField(max_length=15)
    password = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.firstname



class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    # username = models.CharField(max_length=20)
    # image = models.ImageField(upload_to = 'abc',null=True)
    # status = models.CharField(max_length=1000)
    body = models.CharField(max_length=40)
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete = models.DO_NOTHING)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete = models.DO_NOTHING)
    comment = models.TextField(max_length = 50)
 