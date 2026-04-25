from rest_framework import permissions

class IsAdminOrAgent(permissions.BasePermission):
    """
    Custom permission to allow Admins full access, 
    and Agents access to their assigned fields.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins can do everything
        if request.user.role == 'admin':
            return True
        # Agents can only view/update their assigned fields
        return obj.assigned_to == request.user