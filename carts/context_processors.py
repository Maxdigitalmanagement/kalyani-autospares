from carts.models import Cart,CartItem
from carts.views import cart_id

def cart_itemsno(request):
    quantity = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=cart_id(request))
            if request.user.is_authenticated:
                cart_items =  CartItem.objects.all().filter(user = request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            
            for cart_item in cart_items:
                quantity += cart_item.quantity
        except Cart.DoesNotExist:
            quantity = 0

    return dict(cart_items_no = quantity)