from school.models.class_model import Class
from constants.account_strings import AccountStrings
from rest_framework.permissions import BasePermission
from account.models import ParentProfile


class IsParent(BasePermission):
    """
        Checks if the user is a parent.
    """
    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True
    message = AccountStrings.PermissionStrings.is_parent_message


class IsChild(BasePermission):
    """
        Checks if the user is a child.
    """
    def has_permission(self, request, view):
        if request.user.user_type != 2:
            return False
        return True
    message = AccountStrings.PermissionStrings.is_child_message


class IsInstructor(BasePermission):
    """
        Checks if the user is an instructor.
    """
    def has_permission(self, request, view):
        if request.user.user_type != 4:
            return False
        return True
    message = AccountStrings.PermissionStrings.is_instructor_message

class IsInstructorHasSchool(BasePermission):
    """
        Checks whether the user has school information.
    """
    def has_permission(self, request, view):
        if request.user.user_instructor.school is None:
            return False
        return True
    message = AccountStrings.PermissionStrings.is_instructor_has_school_message

class IsOwnChild(BasePermission):
    """
        To edit or destroy a child list record, the user must be owner of that record.
    """
    def has_permission(self, request, view):
        return request.user.user_parent and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (obj.parent == request.user.user_parent) or request.user.is_superuser
    message = AccountStrings.PermissionStrings.is_own_child_message
