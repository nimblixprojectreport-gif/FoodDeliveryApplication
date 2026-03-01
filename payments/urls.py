from django.urls import path
from .views import PaymentCreateView, PaymentListView

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),   # GET
    path('create/', PaymentCreateView.as_view(), name='payment-create'),  # POST
]
