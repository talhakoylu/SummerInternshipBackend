from rest_framework.generics import ListAPIView, RetrieveAPIView
from country.models import City
from country.api.serializers import CitySerializer, CityDetailWithCountrySerializer
from django.shortcuts import get_object_or_404



class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CityDetailAPIView(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailWithCountrySerializer
    
    def get_object(self):
        """
        This overidden method returns a specific city with details.\n
        It needs a special url path e.g city-detail/<country_code>/<city_code>\n
        If the searching object doesn't exists then it returns 404 error.
        """
        obj = get_object_or_404(City,country__code__iexact = self.kwargs["country_code"], code__iexact = self.kwargs["city_code"])
        return obj