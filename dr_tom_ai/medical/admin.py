from django.contrib import admin
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "short_symptoms", "has_image")
    list_filter = ("created_at", "user")
    search_fields = ("symptoms_text", "result_text", "user__username")
    ordering = ("-created_at",)

    def short_symptoms(self, obj):
        return (obj.symptoms_text[:50] + "...") if obj.symptoms_text else "—"
    short_symptoms.short_description = "Symptoms"

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Image Attached"
