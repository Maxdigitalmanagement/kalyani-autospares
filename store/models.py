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
    
    def discount(self):
        if self.price > self.selling_price:
            percentage_discount = int(((self.price - self.selling_price) / self.price) * 100)
            return f'{percentage_discount}% off'

    def __str__(self):
        return self.product_name
    
variation_category_choice = (
    ('color','color'),
)
    
class Variation(models.Model):
    Product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.variation_value
