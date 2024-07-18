from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Account, UserAddress, UserProfile
from carts.models import Cart, CartItem
from carts.views import cart_id
from orders.models import Order, OrderProduct
from store.models import ReviewRating
from .forms import AddressForm, RegistrationForm, UserForm, UserProfileForm
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from kalyaniautospares.settings import EMAIL_HOST_USER

import base64
import requests



# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # Create user profile

            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/profile_empty.svg'
            profile.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = [email]
            send_mail(mail_subject, message, EMAIL_HOST_USER, to_email, fail_silently=True)

            # messages.success(request,'Thank you for registering wth us we have set you a verification email to your email address. please verify it.')

            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
 
    form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/register.html', context)




def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting product varation by cart id
                    product_variation=[]
                    v_ids = []
                    p_qtys = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                        v_ids.append(item.id)
                        p_qtys.append(item.quantity)

                    # get the cart items from the user to access his product vatriation
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []

                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # we need to get the common product variation
                    count = 0
                    delete_ids = []
                    for pr in product_variation:
                        count += 1
                        if pr in ex_var_list:
                            item_id = id[ex_var_list.index(pr)]
                            v_item_id = v_ids[product_variation.index(pr)]
                            qtyty = p_qtys[product_variation.index(pr)]
                            delete_ids.append(v_item_id)
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += qtyty
                            item.user=user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
                    cart_items_to_delete = CartItem.objects.filter(pk__in=delete_ids)
                    cart_items_to_delete.delete()

            except:
                pass
            auth.login(request,user)
            messages.success(request, "you are now logged in.")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout
                params = dict(x.split('=') for x in query.split('&'))
                # it will split into key & value ----> {'next' : '/cart/checkout'}
                if 'next' in params:
                    nextpage = params['next']
                    if "%3F" in nextpage:
                        nextpage = nextpage.replace("%3F", "?")
                    if "%3D" in nextpage:
                        nextpage = nextpage.replace("%3D", "=")
                    return redirect(nextpage)
            except:
                return redirect('profile')

        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')
        

    return render(request, 'accounts/login.html')



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


@login_required(login_url = 'login')
def profile(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    reviews = ReviewRating.objects.order_by('-created_at').filter(user_id=request.user.id)
    reviews_count = reviews.count()
    addresses = UserAddress.objects.order_by('-created_at').filter(user_id=request.user.id)
    addresses_count = addresses.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count' : orders_count,
        'reviews_count' : reviews_count,
        'addresses_count' : addresses_count,
        'userprofile' : userprofile,
    }
    return render(request, 'profile.html', context)
    


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "congratulations! your account is activated")
        return redirect('login')
    else:
        messages.error(request, "invalid activation link")
        return redirect('register')



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = 'html'
            send_email.send()

            messages.success(request, "Password reset email has been set to your email address")
            return redirect('login')
        else:
            messages.error(request,"Account does not exist!")
            return redirect('forgotPassword')
    else:
        return render (request, 'accounts/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, "This link has been expired!")
        return redirect('login')

def resetPassword(request):

    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            if request.user is not None:
                auth.logout(request)
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
        
    else:
        return render(request, 'accounts/resetpassword.html')
        

@login_required(login_url = 'login')
def saveinfo(request):
    user = Account.objects.get(pk=request.user.id)
    userprofile = UserProfile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "your profile is updated.")
            return redirect('profile')
    else :
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
    }
    return render(request, 'profile/myinfo.html', context)
    


@login_required(login_url = 'login')
def myaddresses(request):
    try:
        user_addresses = UserAddress.objects.filter(user=request.user)
    except:
        user_addresses = None
    context = {
        'user_addresses' : user_addresses,
    }
    return render(request, 'profile/myaddresses.html', context)

@login_required(login_url = 'login')
def add_address(request):
    if request.method == 'POST':
        try:
            form = AddressForm(request.POST)
            if form.is_valid():
                data = UserAddress()
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.email = form.cleaned_data['email']
                data.address_line_1 = form.cleaned_data['address_line_1']
                data.address_line_2 = form.cleaned_data['address_line_2']
                data.country = form.cleaned_data['country']
                data.pincode = form.cleaned_data['pincode']
                data.state = form.cleaned_data['state']
                data.city = form.cleaned_data['city']
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Address Added")
                return redirect('myaddresses')
        except:
            messages.error(request, "wrong address")
            return redirect('myaddresses')
    return render(request, 'profile/addaddress.html')

@login_required(login_url = 'login')
def edit_address(request, address_id):
    address = UserAddress.objects.get(id=address_id)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        form.save()
        messages.success(request, "Address updated")
        return redirect('myaddresses')
    else:
        context = {
            'edit_address' : True,
            'address' : address,
        }
        return render(request, 'profile/addaddress.html', context)
    
@login_required(login_url = 'login')
def delete_address(request, address_id):
    address = UserAddress.objects.get(id=address_id)
    is_present = False
    try:
        orders = Order.objects.filter(user_id=request.user.id, is_ordered=True)
        if orders:
            for order in orders:
                if order.address.id == address.id:
                    is_present = True

        if is_present:
            messages.error(request, "you have orders with this address we cannot delete")
            return redirect('myaddresses')
        else:
            name = address.first_name
            address.delete()
            mess = f'{name} address deleted'
            messages.success(request, mess)
            return redirect('myaddresses')
        
    except Order.DoesNotExist:
        name = address.first_name
        address.delete()
        mess = f'{name} address deleted'
        messages.success(request, mess)
        return redirect('myaddresses')


@login_required(login_url = 'login')
def myorders(request):
    new_orders = []
    pro_orders = []
    del_orders = []
    can_orders = []
    try:
        orders = Order.objects.order_by('-created_at').filter(user=request.user,is_ordered=True)
        if orders:
            for order in orders:
                if order.status == "New":
                    new_orders.append(order)
                elif order.status == "Processing":
                    pro_orders.append(order)
                elif order.status == "Delivered":
                    del_orders.append(order)
                elif order.status == "Cancelled":
                    can_orders.append(order)
    except OrderProduct.DoesNotExist:
        order_products = None

    context = {
        'all_orders' : orders,
        'new_orders' : new_orders,
        'pro_orders' : pro_orders,
        'del_orders' : del_orders,
        'can_orders' : can_orders,
    }

    return render(request, 'profile/myorders.html', context)


@login_required(login_url = 'login')
def orderdetails(request, order_id):
        orders = Order.objects.get(id=order_id)
        order_products = OrderProduct.objects.order_by('-created_at').filter(user=request.user,order_id=order_id)

        context = {
            'order' : orders,
            'order_products': order_products,
        }
        return render(request, 'profile/orderdetail.html', context)


@login_required(login_url = 'login')
def myreviews(request):

    reviews = ReviewRating.objects.order_by('-created_at').filter(user=request.user)

    context = {
        'reviews' : reviews,
    }

    return render(request, 'profile/myreviews.html', context)


@login_required(login_url = 'login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Please enter valid current Password")
                return redirect('confirm_password')
        else:
            messages.error(request, "Password does not match!")
            return redirect('confirm_password')
    return render(request, 'accounts/change_password.html')