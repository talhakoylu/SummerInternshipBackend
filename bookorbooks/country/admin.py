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


@admin.register(City)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code", "created_at", "updated_at"]
    list_display_links = ["id", "name", "code"]
    search_fields = ["id", "name", "code"]
    autocomplete_fields = ['country']

    class Meta:
        model = City