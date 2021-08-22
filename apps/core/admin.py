from django.contrib import admin

from apps.core.abc.admin import BaseAdmin
from apps.core.models import TaskControl


@admin.register(TaskControl)
class TaskControlAdmin(BaseAdmin, admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "status",
    )
    list_filter = ("status",)
