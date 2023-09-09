from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from store.forms import ReviewForm

from .models import Product, ReviewRating
from orders.models import OrderProduct
from category.models import Category
from carts.models import Favorites,Cart,CartItem
from carts.views import cart_id
from django.db.models import Q
from django.contrib import messages

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    keywords = ""
    searches = False

    if category_slug != None:
        if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            if keyword:
                categories = get_object_or_404(Category,slug=category_slug)
                products = Product.objects.order_by('-created_date').filter(Q(category=categories), Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(compatible_for__bike_name__icontains=keyword) | Q(belongs_to__belongsto__icontains=keyword))
                paginator = Paginator(products,21)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                product_count = products.count()
                product_filter = categories
                searches = True
                keywords = keyword
        else:
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
        'searched' : searches,
        'keyword' : keywords,
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
    
    try:
        orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    except OrderProduct.DoesNotExist:
        orderproduct=None
    
    context = {
        'single_product' : single_product,
        'favorite' : favorite,
        'in_cart' : in_cart,
        'like_products' : like_products,
        'orderproduct' : orderproduct,
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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted")
                return redirect(url)
