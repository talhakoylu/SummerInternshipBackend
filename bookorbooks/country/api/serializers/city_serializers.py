from country.models.district_model import District
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from country.models import City, Country


class CountryForCityDetailSerializer(serializers.ModelSerializer):
    #helper serializer
    class Meta:
        model = Country
        fields = ["id", "name", "code"]


class DistrictSerializer(serializers.ModelSerializer):
    #helper serializer
    class Meta:
        model = District
        exclude = ["created_at", "updated_at", "country"]


class CitySerializer(serializers.ModelSerializer):
    """
    This serializer returns a json response about City with country and district details
    """
    country = CountryForCityDetailSerializer()
    district = DistrictSerializer()
    class Meta:
        model = City
        exclude = ["created_at", "updated_at"]
