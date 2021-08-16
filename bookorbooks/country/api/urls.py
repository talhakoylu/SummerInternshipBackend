from country.api.views.district_views import DistrictListAPIView
from country.api.views import CountryListAPIView, CountryDetailAPIView, CityListAPIView, CityDetailAPIView
from django.urls import path, re_path

app_name = "country"

urlpatterns = [
    path("country-list", CountryListAPIView.as_view(), name="country-list"),
    path("country-detail/<str:code>", CountryDetailAPIView.as_view(), name="country-detail"),
    path("city-list", CityListAPIView.as_view(), name="city-list"),
    path("city-detail/<country_code>/<city_code>", CityDetailAPIView.as_view(), name="city-detail"),
    path("district-list", DistrictListAPIView.as_view(), name="district_list"),

]
