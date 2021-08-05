from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import ParentProfile, ChildProfile, ChildList

User = get_user_model()


class UserSerializer(ModelSerializer):
    user_type = serializers.CharField(source="get_user_type_display",
                                      read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "first_name", "last_name", "get_full_name",
            "user_type"
        ]


class ChildSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ChildProfile
        fields = ["user"]


class ParentSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ParentProfile
        fields = ["user"]


class ChildListSerializer(ModelSerializer):
    parent = ParentSerializer()
    child = ChildSerializer()

    class Meta:
        model = ChildList
        fields = ["id", "parent", "child"]

class ChildRecordAddSerializer(ModelSerializer):
    class Meta:
        model = ChildList
        exclude = ("parent",)


class ChildrenForDetailSerailizer(ModelSerializer):
    child = ChildSerializer()

    class Meta:
        model = ChildList
        fields = ["id", "child"]

class ChildListByParentSerializer(ModelSerializer):
    user = UserSerializer()
    children = ChildrenForDetailSerailizer(many = True, read_only = True, source = "parent_children")
    class Meta:
        model = ParentProfile
        fields = "__all__"