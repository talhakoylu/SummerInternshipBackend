from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from country.models import City, Country


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class CountryForCityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "code"]


class CityDetailWithCountrySerializer(serializers.ModelSerializer):
    country = CountryForCityDetailSerializer(many=False)

    class Meta:
        model = City
        fields = ["id", "name", "code", "country"]