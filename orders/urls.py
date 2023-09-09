from django.urls import path
from . import views

urlpatterns = [
    path ('place_order/',views.place_order ,name='place_order'),
    path ('payments/',views.payments ,name='payments'),
    path ('order_complete/',views.order_complete ,name='order_complete'),
    path ('generate_invoice_pdf/<int:order_id>/',views.generate_invoice_pdf ,name='generate_invoice_pdf'),
]