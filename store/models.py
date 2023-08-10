from django.db import models
from django.urls import reverse
from category.models import Category,Bike,PartBelongs

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    selling_price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    compatible_for = models.ForeignKey(Bike, on_delete=models.CASCADE)
    belongs_to = models.ForeignKey(PartBelongs,blank=True, on_delete=models.CASCADE,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    material=models.CharField(max_length=100,blank=True)
    color=models.CharField(max_length=50,blank=True)
    part_number=models.CharField(max_length=100,unique=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug,self.slug])


    def __str__(self):
        return self.product_name