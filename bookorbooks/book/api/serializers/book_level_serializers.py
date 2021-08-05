from rest_framework import serializers
from book.models import BookLevel


class BookLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLevel
        fields = "__all__"



