from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Product
from category.models import Category
from carts.models import Favorites,Cart,CartItem
from carts.views import cart_id
from django.db.models import Q

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories, is_available = True)
        paginator = Paginator(products,21)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        product_filter = categories
    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,21)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        product_filter = None

    index = paged_products.number -1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'products': paged_products,
        'product_count' : product_count,
        'product_filter': product_filter,
        'searched' : False,
        'keyword' : "",
        'page_range': page_range,
    }

    return render(request,'search_result.html',context)


def product_detail(request, category_slug=None, product_slug=None):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug )
        like_products = Product.objects.filter(compatible_for=single_product.compatible_for)
        
        favorite = Favorites.objects.filter(product=single_product, cart__cart_id=cart_id(request)).exists()
        in_cart = CartItem.objects.filter(product=single_product, cart__cart_id=cart_id(request)).exists()

    except Exception as e:
        raise e
    
    context = {
        'single_product' : single_product,
        'favorite' : favorite,
        'in_cart' : in_cart,
        'like_products' : like_products,
    }


    return render(request, 'productpage.html', context)



def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(compatible_for__bike_name__icontains=keyword) | Q(belongs_to__belongsto__icontains=keyword))
            paginator = Paginator(products,21)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
            product_filter = None
    
    index = paged_products.number -1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'products': paged_products,
        'product_count' : product_count,
        'product_filter': product_filter,
        'searched' : True,
        'keyword' : keyword,
        'page_range': page_range,
    }

    return render(request,'search_result.html', context)