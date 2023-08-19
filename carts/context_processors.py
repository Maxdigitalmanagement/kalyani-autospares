from carts.models import Cart,CartItem
from carts.views import cart_id

def cart_items_no(request):
    quantity = 0
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            quantity += cart_item.quantity
    except Cart.DoesNotExist:
        pass

    return dict(cart_items = quantity)