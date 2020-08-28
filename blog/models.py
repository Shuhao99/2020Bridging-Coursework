from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length = 100,default='cat_test')
    def __str__(self):
        return self.name
   


class Tag(models.Model):
    name = models.CharField(max_length=100,default='tag_test')
    def __str__(self):
        return self.name
   


class Post(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header_img = models.ImageField(null = True, blank=True, upload_to="images/")
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=500, blank = True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    is_slide = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class about(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name


        
