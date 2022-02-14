from multiprocessing import Condition
from rest_framework import permissions

class IsOwnerAndReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.id == request.user.id:
            return True
        if request.method in ('DELETE',) and request.user.is_staff:
            return True    
        return False

    
    