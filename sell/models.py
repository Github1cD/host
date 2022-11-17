from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()


class Seller(models.Model):
    seller_id = models.CharField(
        max_length = 20,
        primary_key = True,
        )
    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        )
    rating = models.IntegerField(default = 5)
    mobile = models.CharField(max_length = 10)
    
    def __str__(self):
        return self.user.first_name

    
class Products(models.Model):
    #product_id = 
    product_name = models.CharField(max_length= 40)
    product_image = models.ImageField(upload_to='products/',default='products/dummy.jpg')  
    description = models.CharField(max_length=500,default='description not available')
    total_quantity = models.IntegerField(default =0)
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE)
    price = models.IntegerField(default = 0)
    
    
    def __str__(self):
        return self.product_name
    
