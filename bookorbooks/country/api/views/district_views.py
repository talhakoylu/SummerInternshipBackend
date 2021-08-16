from country.api.serializers.district_serializers import DistrictSerializer
from country.models.district_model import District
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter


class DistrictListAPIView(ListAPIView):
    """
    Returns the list of all districts with city and country details.
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [SearchFilter]
    search_fields = ['country__name', 'country__code', 'name', 'district_cities__name']