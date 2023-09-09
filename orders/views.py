import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from carts.models import CartItem
from store.models import Product
from .models import Order, OrderProduct, Payment
from accounts.models import UserAddress
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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





from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image
from reportlab.platypus.flowables import PageBreak

def generate_invoice_pdf(request, order_id):
    # Fetch order details based on order_id
    order = get_object_or_404(Order, order_number=order_id)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

    # Create a PDF document with landscape orientation
    doc = SimpleDocTemplate(response, pagesize=landscape(letter))

    # Create a list to hold the elements of the PDF
    elements = []

    # Define styles for the PDF
    styles = getSampleStyleSheet()

    # Add Flipkart-like header
    header = Image("path/to/flipkart-logo.png", width=200, height=60)
    header.hAlign = 'CENTER'
    elements.append(header)

    # Add some space
    elements.append(Spacer(1, 36))

    # Create a Table for order details
    data = [
        ["Order Number:", f"{order_id}"],
        ["Order Date:", f"{order.date}"],
        ["Shipping Address:", f"{order.full_name},\n{order.address_line_1}\n,{order.address_line_2}\n,{order.city}\n,{order.state}\n,{order.country} - {order.pincode}"],
        # Add more details as needed
    ]

    # Define table style
    table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ])

    # Create the table
    order_table = Table(data, colWidths=[150, 300])
    order_table.setStyle(table_style)

    # Add the table to the PDF elements
    elements.append(order_table)

    # Add some space
    elements.append(Spacer(1, 36))

    order_items = OrderProduct.objects.filter(order=order,user=request.user)
    # Create a table for displaying order items

    item_data = [
        ["Product", "Price", "Quantity", "Total"],
    ]

    for items in order_items:
        item_data.append([items.product.product_name,items.product_price,items.quantity,items.product_price*items.quantity])

    # Define table style for items
    item_table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ])

    # Create the item table
    item_table = Table(item_data, colWidths=[250, 70, 70, 70])
    item_table.setStyle(item_table_style)

    # Add the item table to the PDF elements
    elements.append(item_table)

    # Add some space
    elements.append(Spacer(1, 36))

    # Add total amount
    total_amount = Paragraph("<b>Total Amount:</b> $130.00", styles['Normal'])
    elements.append(total_amount)

    # Build the PDF document
    doc.build(elements)

    return response

