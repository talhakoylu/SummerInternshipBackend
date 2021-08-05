from constants.account_strings import AccountStrings
from rest_framework.permissions import BasePermission


class IsOwnClass(BasePermission):
    """
        To edit a record from class table, the user must be the owner of the class.
    """
    def has_object_permission(self, request, view, obj):
        return (obj.instructor == request.user.user_instructor) # or request.user.is_superuser
    message = AccountStrings.PermissionStrings.is_own_class_message


class IsOwnStudent(BasePermission):
    """
        To edit a record from student list table, the user must be the owner of the class.
    """
    def has_object_permission(self, request, view, obj):
        return (obj.school_class.instructor == request.user.user_instructor) or request.user.is_superuser
    message = AccountStrings.PermissionStrings.is_own_class_message
