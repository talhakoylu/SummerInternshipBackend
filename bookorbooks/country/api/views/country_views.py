from rest_framework.generics import ListAPIView, RetrieveAPIView
from country.models import Country
from country.api.serializers import CountrySerializer, CountryDetailWithCitySerializer


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDetailAPIView(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailWithCitySerializer
    lookup_url_kwarg = 'code'
    lookup_field = 'code__iexact'