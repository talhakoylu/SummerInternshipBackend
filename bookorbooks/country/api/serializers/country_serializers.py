from rest_framework.fields import SerializerMethodField
from country.models import Country, City
from rest_framework import serializers

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class CityForCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "code"]

class CountryDetailWithCitySerializer(serializers.ModelSerializer):
    cities = SerializerMethodField()
    class Meta:
        model = Country
        fields = ["id", "name", "code", "cities"]

    def get_cities(self, obj):
        ordered_cities = obj.cities.order_by("code")
        return CityForCountrySerializer(ordered_cities, many = True).data