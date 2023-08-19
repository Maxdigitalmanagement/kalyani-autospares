from django.shortcuts import render
from store.models import Product
from carts.models import Favorites,Cart,CartItem
from carts.views import cart_id

def home(request):
    products=Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request,'index.html', context)