from account.api.views.child_list_views import ChildListByUserAPIView, ChildListItemDestroyAPIView
from django.urls.conf import include
from account.api.views.account_views import PasswordUpdateAPIView
from account.api.views.profile_views import ChildProfileUpdateAPIView, InstructorProfileUpdateAPIView, MeAPIView, ParentProfileUpdateAPIView
from django.urls import path
from account.api.views import CreateUserAPIView, ChildListAPIView, ChildListCreateAPIView

app_name = "account"

urlpatterns = [
    path("register", CreateUserAPIView.as_view(), name="register"),
    path("update-password", PasswordUpdateAPIView.as_view(), name="update_password"),
    path("child-list", ChildListAPIView.as_view(), name="child_list"),
    path("child-list-by-parent", ChildListByUserAPIView.as_view(), name="child_list_detail"),
    path("add-child-record", ChildListCreateAPIView.as_view(), name="child_list_create"),
    path("destroy-child-record/<child_id>", ChildListItemDestroyAPIView.as_view(), name="child_list_item_destroy"),
    path("child-profile-update", ChildProfileUpdateAPIView.as_view(), name="child_profile_update"),
    path("parent-profile-update", ParentProfileUpdateAPIView.as_view(), name="parent_profile_update"),
    path("instructor-profile-update", InstructorProfileUpdateAPIView.as_view(), name="instructor_profile_update"),
    path("me", MeAPIView.as_view(), name = "me")
    
]
