from django.contrib import admin
from competencies.models import (Configuration)


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('ldss_host',)
