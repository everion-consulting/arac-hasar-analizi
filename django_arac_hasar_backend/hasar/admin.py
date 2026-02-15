from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import HasarTahmin


class HasarTahminResource(resources.ModelResource):
    class Meta:
        model = HasarTahmin
        # İstersen buraya include/exclude, export_order vs. ekleyebilirsin


@admin.register(HasarTahmin)
class HasarTahminAdmin(ImportExportModelAdmin):
    resource_class = HasarTahminResource
    list_display = (
        "created_at",
        "marka",
        "model",
        "arac_turu",
        "rayic_bedel",
        "hasar_bedeli",
        "tahmini",
        "min_deger",
        "max_deger",
    )
