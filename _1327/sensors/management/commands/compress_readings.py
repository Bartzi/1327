from django.core.management.base import BaseCommand
from django.db.models import Avg
from django.db.models.functions import TruncDay

from _1327.sensors.models import Sensor, SensorReading


class Command(BaseCommand):
	help = 'Compress Sensor Readings.'

	def handle(self, *args, **options):
		sensors = Sensor.objects.all()

		for sensor in sensors:
			# get average reading per day
			averages_per_day = (
				SensorReading.objects
				.filter(sensor=sensor)
				.annotate(compressed_time=TruncDay('time'))
				.values('compressed_time')
				.annotate(average=Avg('value'))
				.values('compressed_time', 'average')
			)
			# delete old readings
			sensor.readings.all().delete()

			# save averages
			for reading in averages_per_day:
				new_reading = SensorReading.objects.create(
					sensor=sensor,
					time=reading['compressed_time'],
					value=reading['average']
				)
				new_reading.save()
