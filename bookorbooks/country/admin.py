from country.models.district_model import District
from country.models.city_model import City
from django.contrib import admin
from country.models import Country
# Register your models here.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "created_at", "updated_at"]
    list_display_links = ["id", "name", "code"]
    search_fields = ["id", "name", "code"]
    search_fields = ['name', "code"]

    class Meta:
        model = Country


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "created_at", "updated_at"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name", "country__name"]
    autocomplete_fields = ['country']

    class Meta:
        model = District


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "district", "country", "created_at", "updated_at"]
    list_display_links = ["id", "name", "code"]
    search_fields = ["id", "name", "code", "district__name"]
    autocomplete_fields = ['country', "district"]

    class Meta:
        model = City