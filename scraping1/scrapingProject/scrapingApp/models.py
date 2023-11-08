from django.db import models

# Create your models here.
class UserProfileInfo(models.Model):

    username=models.CharField(max_length=264)
    password=models.CharField(max_length=264)
    email=models.EmailField(max_length=264,unique=True)
    def __str__(self):
        return self.username

class MovieInfo(models.Model):
    moviename=models.CharField(max_length=264)
    movieyear=models.CharField(max_length=264)
    movietime=models.CharField(max_length=264)
    movierating=models.CharField(max_length=264)
    movieurl=models.URLField()
    moviedirector=models.CharField(max_length=264)
    directorurl=models.URLField()
    topMovie=models.CharField(max_length=264)


