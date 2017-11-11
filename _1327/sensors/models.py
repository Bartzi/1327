import uuid

from django.db import models


class Sensor(models.Model):

	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	unit_of_measurement = models.CharField(max_length=10, default='°C')

	def latest_reading(self):
		reading = self.readings.order_by('-time').first()
		return "{} {}".format(reading.value, self.unit_of_measurement)

	def __str__(self):
		return self.name


class SensorReading(models.Model):

	sensor = models.ForeignKey(Sensor, related_name='readings')
	time = models.DateTimeField(auto_now_add=True)
	value = models.FloatField(default=0)

	def __str__(self):
		return "{value} {unit} at {time}".format(
			value=self.value,
			unit=self.sensor.unit_of_measurement,
			time=self.time.strftime("%Y-%m-%d %H:%M.%S"),
		)
