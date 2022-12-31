from django.db import models
import hashlib

class UserModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=20)
    logged_in = models.BooleanField(default=False)        
