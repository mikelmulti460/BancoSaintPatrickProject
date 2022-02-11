from rest_framework import permissions

class UpdateUserData(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        condition = request.user.is_staff == True
        if request.method in permissions.SAFE_METHODS and obj.id == request.user.id or condition:
            return True
            
        return condition