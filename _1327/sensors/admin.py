from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from _1327.sensors.models import Sensor, SensorReading


class SensorModelAdmin(GuardedModelAdmin):

	list_display = ('uuid', 'name', 'unit_of_measurement')


admin.site.register(Sensor, SensorModelAdmin)
admin.site.register(SensorReading)
