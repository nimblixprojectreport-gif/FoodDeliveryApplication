from rest_framework.permissions import BasePermission

class IsDeliveryPartner(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "DELIVERY"