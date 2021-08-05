from rest_framework import serializers
from book.models import BookLanguage


class BookLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLanguage
        fields = "__all__"
