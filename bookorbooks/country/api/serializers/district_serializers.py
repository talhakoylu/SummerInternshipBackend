from rest_framework.serializers import ModelSerializer
from country.models import City, Country, District

class CountrySerializer(ModelSerializer):
    #helper serializer
    class Meta:
        model = Country
        exclude = ["created_at", "updated_at"]

class CitySerializer(ModelSerializer):
    #helper serializer
    class Meta:
        model = City
        exclude = ["created_at", "updated_at", "district", "country"]

class DistrictSerializer(ModelSerializer):
    """
    This serializer gives a response model about Districts that the model have country and city details.
    """
    country = CountrySerializer(many = False)
    cities = CitySerializer(many = True, source = "district_cities")
    class Meta:
        model = District
        exclude = ["created_at", "updated_at"]