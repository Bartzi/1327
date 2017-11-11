from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

# Create your views here.
from guardian.shortcuts import get_objects_for_user

from _1327.sensors.models import Sensor, SensorReading


def index(request):
	sensors = get_objects_for_user(request.user, 'sensors.change_sensor')
	return render(
		request,
		'sensors_index.html',
		{
			'sensors': sensors,
		}
	)


def details(request, uuid):
	sensor = Sensor.objects.get(uuid=uuid)
	if not request.user.has_perm('sensors.change_sensor', sensor):
		raise PermissionDenied

	readings = sensor.readings.order_by('time')

	return render(
		request,
		'sensors_details.html',
		{
			'sensor': sensor,
			'times': [reading.time.strftime("%Y-%m-%d %H:%M.%S") for reading in readings],
			'values': [reading.value for reading in readings],
		}
	)


def update(request, uuid):
	sensor = get_object_or_404(Sensor, uuid=uuid)
	value = request.GET['value']
	reading = SensorReading(sensor=sensor, value=value)
	reading.save()

	return HttpResponse()
