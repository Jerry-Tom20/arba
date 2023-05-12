
from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField

# Create your models here.

class usermember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    user_image = models.ImageField(upload_to='image/',null=True)
    user_accepter = models.BooleanField(null=True)

class categories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    cat_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/', null=True)
    cat_slug = AutoSlugField(populate_from='cat_name',unique=True, null=True,default=None)
    
class products(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    cat = models.ForeignKey(categories, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    pro_image = models.ImageField(upload_to='image/', null=True)
    pro_slug = AutoSlugField(populate_from='title',unique=True, null=True,default=None)
    
class cart1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(products, on_delete=models.CASCADE,null=True)
    qty=models.IntegerField()


