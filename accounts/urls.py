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

    path('infoverify/',views.infoverify, name='infoverify'),
    path('myinfo/',views.myinfo, name='myinfo'),
    path('saveinfo/',views.saveinfo, name='saveinfo'),

]