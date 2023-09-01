from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Cart, CartItem,Favorites
from django.contrib.auth.decorators import login_required

from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.

def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request):

    current_user = request.user

    product_id = request.POST['product_id']
    items_qty = int(request.POST['quantity'])

    # if user is authenticated
    if current_user.is_authenticated:

        try:
            addedfromfav = int(request.POST['addedfromfav'])
        except:
            addedfromfav = 0

        product = Product.objects.get(id=product_id)
        product_variation=[]

        if request.method == 'POST' :
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(Product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists=CartItem.objects.filter(product=product,user=current_user).exists()

        if is_cart_item_exists :
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                #increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += items_qty
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=items_qty, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = items_qty,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        
        if addedfromfav > 0:
            favorites_items = Favorites.objects.filter(product=product, user=current_user)
            favorites_items.delete()
        
        return redirect('cart')


    # if the user is not authenticated

    else:
        
        try:
            addedfromfav = int(request.POST['addedfromfav'])
        except:
            addedfromfav = 0

        product = Product.objects.get(id=product_id)
        product_variation=[]

        if request.method == 'POST' :
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(Product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart = Cart.objects.get(cart_id=cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=cart_id(request)
            )
        cart.save()

        is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()

        if is_cart_item_exists :
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing variations -> database
            # current variation -> product_variations list
            # item_id -> database
            ex_var_list = []
            id = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                #increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += items_qty
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=items_qty, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = items_qty,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        
        if addedfromfav > 0:
            favorites_items = Favorites.objects.filter(product=product, cart=cart)
            favorites_items.delete()
        
        return redirect('cart')
    

# add_cart ended


def minus_cart(request):

    cart_item_id = request.GET.get('cart_item_id')
    product_id = request.GET.get('product_id')

    product = Product.objects.get(id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def delete_cart(request):
    
    cart_item_id = request.GET.get('cart_item_id')
    product_id = request.GET.get('product_id')

    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()

    return redirect('cart') 



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity':quantity,
        'cart_items':cart_items,
    }
    request.session['cart_items_no'] = quantity
    return render(request, 'cart.html', context)




@login_required(login_url = 'login')
def favorites(request):
    items = 0
    favorites_items = 0
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        favorites_items = Favorites.objects.filter(cart=cart, is_active=True)
        items=len(favorites_items)
    except ObjectDoesNotExist:
        pass

    

    context = {
        'items' : items,
        'favorites_items':favorites_items,
    }

    return render(request, 'favorites.html', context)



@login_required(login_url = 'login')
def add_favorites(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=cart_id(request)
        )
    cart.save()

    favorite_item = Favorites.objects.create(
        product = product,
        cart = cart,
    )
    favorite_item.save()
    
    return redirect(product.get_url())

def move_to_cart(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=cart_id(request))
    favorites_items = Favorites.objects.filter(product=product, cart=cart)
    try :
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if(cart_item.quantity<10):
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist :
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    favorites_items.delete()
    
    return redirect('cart')

def delete_favorites(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=cart_id(request))
    favorites_items = Favorites.objects.filter(product=product, cart=cart)
    favorites_items.delete()
    return redirect(product.get_url())



@login_required(login_url = 'login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity':quantity,
        'cart_items':cart_items,
    }
    return render(request, 'checkout.html', context)

