from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.models import Account
from carts.models import Cart, CartItem
from carts.views import cart_id
from .forms import RegistrationForm
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = 'html'
            send_email.send()

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
    return render(request, 'profile.html')
    


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
def infoverify(request):

    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            return redirect('myinfo')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('infoverify')
    else:
        return render(request, 'accounts/authenticateinfo.html')


@login_required(login_url = 'login')
def myinfo(request):
    return render(request, 'accounts/myinfo.html')

@login_required(login_url = 'login')
def saveinfo(request):
    user = Account.objects.get(pk=request.user.id)

    if request.method == 'POST':
        try:
            if request.POST['last_name']:
                user.last_name = request.POST['last_name']
        except:
            pass
        try:
            if request.POST['first_name']:
                user.first_name = request.POST['first_name']
        except:
            pass
        try:
            if request.POST['phone']:
                user.phone_number = request.POST['phone']
        except:
            pass
        user.save()
        return redirect('profile')