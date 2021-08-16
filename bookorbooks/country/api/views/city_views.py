from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from country.models import City
from country.api.serializers import CitySerializer
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter


class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['country__name', 'country__code', 'name', 'district__name']
    filterset_fields = ['country', 'district']


class CityDetailAPIView(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
    def get_object(self):
        """
        This overridden method returns a specific city with details.\n
        It needs a special url path e.g city-detail/<country_code>/<city_code>\n
        If the searching object doesn't exists then it returns 404 error.
        """
        obj = get_object_or_404(City,country__code__iexact = self.kwargs["country_code"], code__iexact = self.kwargs["city_code"])
        return obj