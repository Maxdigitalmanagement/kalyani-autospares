import datetime
from io import BytesIO
import uuid
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from carts.models import CartItem
from store.models import Product
from .models import Order, OrderProduct, Payment
from accounts.models import UserAddress
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


# Create your views here.


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user = request.user, is_ordered=False, order_number = body["orderID"])
    
    # store transaction details inside payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to order product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.selling_price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # reduce the quantity of sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -=item.quantity
        product.save()

    # clear the cart
    CartItem.objects.filter(user=request.user).delete()

    # send order received mail to the customer
    order_items = OrderProduct.objects.filter(user=request.user,order=order)
    mail_subject = 'Thank you for your order'
    message = render_to_string('orders/order_received_email.html',{
        'user' : request.user,
        'order' : order,
        'order_items' : order_items,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = 'html'
    send_email.send()

    # send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number' : order.order_number,
        'transID' : payment.payment_id,
    }
    return JsonResponse(data)



def place_order(request):
    current_user = request.user

    # if the cart count is lessthan or equal to zero the redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    

    grand_total = 0
    tax_charges = 0
    total = 0
    quantity = 0

    for cart_item in cart_items:
        total += (cart_item.product.selling_price * cart_item.quantity)
        quantity += cart_item.quantity


    grand_total = total + tax_charges

    if request.method == 'POST':
        # store all the billing information inside the order table
        addr_id = request.POST['addr_id']
        address = UserAddress.objects.get(pk=addr_id)

        data = Order()
        data.user = current_user
        data.address = address
        data.order_total = grand_total
        data.tax = tax_charges
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        order_number = "KAORDR"+current_date + str(data.id)
        data.order_number = order_number
        data.save()

        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        context = {
            'order' : order,
            'cart_items' : cart_items,
            'total' : total,
            'tax_charges' : tax_charges,
            'grand_total' : grand_total,
            'address' : address
        }
        return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        payment = Payment.objects.get(payment_id=transID, order=order)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price*i.quantity

        context = {
            'order' : order,
            'order_items' : ordered_products,
            'payment' : payment,
            'subtotal' : subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist) :
        return redirect('home')
    

def generate_invoice_pdf(request, order_id):
    # Replace this with your logic to generate the invoice HTML from your template
    order = Order.objects.get(id=order_id, is_ordered=True)
    ordered_products = OrderProduct.objects.order_by("-created_at").filter(order_id=order.id)
    context = {
        'order': order,
        'order_products' : ordered_products,
    }

    template = get_template('orders/invoice_template.html')
    html = template.render(context)

    # Create a BytesIO buffer to hold the PDF data
    response = BytesIO()

    # Generate the PDF and store it in the response buffer
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)

    # Check if PDF generation was successful
    if not pdf.err:
        # Set the response content type to PDF
        response.seek(0)
        response = HttpResponse(response.read(), content_type='application/pdf')

        # Set content disposition to force download
        response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}_{uuid.uuid4()}.pdf"'

        return response
    else:
        return HttpResponse('PDF generation error', status=500)
    