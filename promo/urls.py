from django.urls import path
from .views import PromoValidateView

urlpatterns = [
    path('validate/', PromoValidateView.as_view(), name='promo-validate'),
]
