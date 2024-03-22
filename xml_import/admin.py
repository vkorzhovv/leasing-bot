from django.contrib import admin
from .models import XMLImportSettings, ImportStatistics
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule, PeriodicTask
from django_celery_beat.admin import PeriodicTaskAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(XMLImportSettings)
class XMLImportSettingsAdmin(admin.ModelAdmin):
    list_display = ('folder_path', 'file_name')

    def has_add_permission(self, request):
        return False


@admin.register(ImportStatistics)
class ImportStatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'imported', 'updated', 'skipped')


class PeriodicTaskAdmin(PeriodicTaskAdmin):
    """Admin-interface for periodic tasks."""

    fieldsets = (
        (None, {
            'fields': ('name', 'regtask', 'task', 'enabled', 'description',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Schedule'), {
            'fields': ('crontab',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Arguments'), {
            'fields': ('args', 'kwargs'),
            'classes': ('extrapretty', 'wide', 'collapse', 'in'),
        }),
        (_('Execution Options'), {
            'fields': ('expires', 'expire_seconds', 'queue', 'exchange',
                       'routing_key', 'priority', 'headers'),
            'classes': ('extrapretty', 'wide', 'collapse', 'in'),
        }),
    )
    


admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)


admin.site.register(PeriodicTask, PeriodicTaskAdmin)