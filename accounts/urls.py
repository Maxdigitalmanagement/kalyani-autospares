from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),

    path('profile/',views.profile, name='profile'),
    path('',views.profile, name='profile'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    

    path('forgotPassword/',views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/',views.resetPassword, name='resetPassword'),

    path('saveinfo/',views.saveinfo, name='saveinfo'),
    path('myaddresses/',views.myaddresses, name='myaddresses'),
    path('add_address/',views.add_address, name='add_address'),
    path('delete_address/<int:address_id>',views.delete_address, name='delete_address'),
    path('edit_address/<int:address_id>',views.edit_address, name='edit_address'),
    path('myorders/',views.myorders, name='myorders'),
    path('orderdetails/<int:order_id>',views.orderdetails, name='orderdetails'),
    path('myreviews/',views.myreviews, name='myreviews'),
    path('change_password/',views.change_password, name='change_password'),

]