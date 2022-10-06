from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator
from django.contrib.auth.models import User
from user_app.models import Account

# Create your models here.

class Business(models.Model):
  
  name = models.CharField(max_length=250)
  website = models.URLField(max_length=250)
  active = models.BooleanField(default=True)

  def __str__(self):
    return self.name


class Propertys(models.Model):

  direction = models.CharField(max_length=250)
  country = models.CharField(max_length=150)
  description = models.CharField(max_length=500)
  thumbnail = models.CharField(max_length=900)
  active = models.BooleanField(default=True)
  avg_calification = models.FloatField(default=0)
  number_calification = models.IntegerField(default=0)
  business = models.ForeignKey(Business,on_delete=models.CASCADE,
              related_name="edificationslist")
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.direction

class Comment(models.Model):

  comment_user = models.ForeignKey(Account,on_delete=models.CASCADE)
  calification = models.PositiveIntegerField(validators=[MinValueValidator(1)
                  ,MaxValueValidator(5)])
  content = models.CharField(max_length=200,null=True)
  propertys = models.ForeignKey(Propertys,on_delete=models.CASCADE,
                  related_name='comments')
  active = models.BooleanField(default=True)
  created_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.calification) + " " + self.propertys.direction #str(self.comment_user)
