from django.shortcuts import get_object_or_404, render

from .models import Product
from category.models import Category

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories, is_available = True)
        product_count = products.count()
        product_filter = categories
    else:
        products=Product.objects.all().filter(is_available=True)
        product_count = products.count()
        product_filter = None

    context = {
        'products': products,
        'product_count' : product_count,
        'product_filter': product_filter,
    }

    return render(request,'search_result.html',context)


def product_detail(request, category_slug=None, product_slug=None):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug )
        like_products = Product.objects.filter(compatible_for=single_product.compatible_for)
    except Exception as e:
        raise e
    

    
    context = {
        'single_product' : single_product,
        'like_products' : like_products,
    }


    return render(request, 'productpage.html', context)