from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )

class IsStaffOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Персонал бачить усе
        if request.user.is_staff:
            return True
        # Користувач бачить тільки свої ордери (і відповідно квитки)
        return obj.user == request.user

    def has_permission(self, request, view):
        # Для списку і detail перевірка буде в has_object_permission
        # Але для списку потрібно фільтрувати queryset
        return request.user and request.user.is_authenticated