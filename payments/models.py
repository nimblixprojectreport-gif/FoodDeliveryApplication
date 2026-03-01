from django.db import models
from orders.models import Order

class Payment(models.Model):

    PAYMENT_METHODS = (
        ('COD', 'Cash On Delivery'),
        ('CARD', 'Card'),
        ('UPI', 'UPI'),
    )

    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order.id} - {self.payment_method}"
