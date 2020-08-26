from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser

class about(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name
    

class experience(models.Model):
    experience_title = models.TextField()
    experience_name = models.TextField(default='Intern')
    experience_text = models.TextField()
    experience_date_start = models.CharField(max_length=100, default='September 2010')
    experience_date_end = models.CharField(max_length=100, default='September 2010')
    def __str__(self):
        return self.experience_title



class education(models.Model):
    facility = models.CharField(max_length=100, default='UNNC')
    title = models.CharField(max_length = 50, default='BSc Student')
    Grade = models.CharField(max_length = 100, default='4.00')
    date_start = models.CharField(max_length=100, default='September 2010')
    date_end = models.CharField(max_length=100, default='September 2010')
    def __str__(self):
        return self.facility
    


class skills(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name

class award(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name
