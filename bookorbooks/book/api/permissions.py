from constants.book_strings import BookStrings
from constants.account_strings import AccountStrings
from rest_framework.permissions import BasePermission


class IsParentOrInstructor(BasePermission):
    """
        Checks if the user is a parent or an instructor.
    """
    def has_permission(self, request, view):
        if request.user.user_type == 3 or request.user.user_type == 4 or request.user.is_superuser:
            return True
        return False
    message = BookStrings.PermissionStrings.is_parent_or_instructor