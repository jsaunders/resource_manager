from django.contrib import admin

from .models import Resource, Lease


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name','key','path','next_time_available','available','booked_by')

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('resource','start_time','end_time','user')
    pass
