from django.db import models
from register.models import UserModel

# Create your models here.
class ProductModel(models.Model):
    product_name = models.CharField(max_length=100)    
    quantity = models.CharField(max_length=100)
    price = models.FloatField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)