from django.contrib import admin, messages
from django.utils import timezone
from .models import Detail, User

@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    search_fields = ['imei', 'alarm_code']
    list_display = ['imei', 'alarm_code', 'formatted_alarm_time']
    ordering = ['alarm_time']

    def formatted_alarm_time(self, obj: Detail):
        return timezone.datetime.fromtimestamp(obj.alarm_time).strftime('%Y-%m-%d %H:%M:%S')
    formatted_alarm_time.admin_order_field = 'alarm_time'
    formatted_alarm_time.short_description = 'Alarm Time'

def make_tracking(modeladmin, request, queryset):
    queryset.update(is_tracking=True)
    modeladmin.message_user(
        request,
        "El seguimiento de los usuarios seleccionados ha sido habilitado.",
        messages.SUCCESS
    )
make_tracking.short_description = "Habilitar seguimiento para usuarios seleccionados"

def make_not_tracking(modeladmin, request, queryset):
    queryset.update(is_tracking=False)
    modeladmin.message_user(
        request,
        "El seguimiento de los usuarios seleccionados ha sido deshabilitado.",
        messages.SUCCESS
    )
make_not_tracking.short_description = "Deshabilitar seguimiento para usuarios seleccionados"

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['user_name', 'car_owner', 'imei']
    list_display = ['user_name', 'imei', 'license_number','is_tracking']
    ordering = ['account_id']
    actions = [make_tracking, make_not_tracking]
