from competencies.models import (
    Configuration,
    DjangoDomain,
)
from django.contrib import admin


@admin.register(DjangoDomain)
class DjangoDomainAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name")
    list_filter = ("name",)
    search_fields = ("name", "uuid")


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ("ldss_host",)
