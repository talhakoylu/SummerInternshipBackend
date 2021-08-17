from account.models.instructor_model import InstructorProfile
from account.models.child_list_model import ChildList
from django.core.checks.messages import Error
from account.models.parent_profile_model import ParentProfile
from django import forms
from account.models.custom_user_model import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import ChildProfile

from .forms import CustomUserCreationForm, CustomUserChangeForm


class ChildProfileAdminForm(forms.ModelForm):
    """
    This class is overrides the description field. In this way, user sees a textfield area
    instead of charfield area.
    """
    class Meta:
        model = ChildProfile
        fields = "__all__"
        widgets = {"hobbies": forms.Textarea(attrs={'cols': 80, 'rows': 10})}


class ParentProfileAdminForm(forms.ModelForm):
    """
    This class is overrides the description field. In this way, user sees a textfield area
    instead of charfield area.
    """
    class Meta:
        model = ParentProfile
        fields = "__all__"
        widgets = {
            "profession": forms.Textarea(attrs={
                'cols': 80,
                'rows': 10
            })
        }


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = ((None, {
        'fields': (('first_name', 'last_name'), ('username', 'email'),
                   ('password1', 'password2'), ('gender', 'user_type', 'identity_number')),
    }), )
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'id', 'email', 'username', 'first_name', 'last_name', 'gender',
        'user_type'
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {
        'fields': ('identity_number', 'gender', 'birth_date', 'user_type')
    }), )

    list_display_links = ["id", "email"]


@admin.register(ChildProfile)
class ChildProfileAdmin(admin.ModelAdmin):
    model = ChildProfile
    form = ChildProfileAdminForm
    list_display = ["pk", "full_name", "user_email", "user_gender"]
    list_display_links = ["pk", "full_name"]

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"

    def user_gender(self, obj):
        return obj.user.get_gender_display()

    user_gender.short_description = "Cinsiyet"

    def full_name(self, obj):
        return obj.get_full_name

    full_name.short_description = "İsim Soyisim"


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    model = ParentProfile
    form = ParentProfileAdminForm
    list_display = ["pk", "full_name", "user_email", "user_gender"]
    list_display_links = ["pk", "full_name"]

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"

    def user_gender(self, obj):
        return obj.user.get_gender_display()

    user_gender.short_description = "Cinsiyet"

    def full_name(self, obj):
        return obj.get_full_name

    full_name.short_description = "İsim Soyisim"


@admin.register(ChildList)
class ChildListModel(admin.ModelAdmin):
    model = ChildList
    list_display = ["id", "get_parent", "get_child"]
    list_display_links = ["id", "get_parent"]

    def get_parent(self, obj):
        return obj.parent.get_full_name
    get_parent.admin_order_field  = 'parent'  
    get_parent.short_description = 'Parent'  
    
    
    def get_child(self, obj):
        return obj.child.get_full_name
    get_child.admin_order_field  = 'child'  
    get_child.short_description = 'Child'  


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    model = InstructorProfile
    list_display = ["pk", "full_name", "instructor_school", "user_email", "user_gender"]
    list_display_links = ["pk", "full_name"]

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"

    def user_gender(self, obj):
        return obj.user.get_gender_display()

    user_gender.short_description = "Cinsiyet"

    def full_name(self, obj):
        return obj.get_full_name

    full_name.short_description = "İsim Soyisim"
    
    def instructor_school(self, obj):
        return obj.school

    instructor_school.short_description = "Okul"