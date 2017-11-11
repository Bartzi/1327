from django.conf.urls import url

from _1327.sensors import views

app_name = "sensors"

urlpatterns = [
	url(r"list$", views.index, name="index"),
	url(r'(?P<uuid>[\d\-a-f]+)/details', views.details, name='details'),
	url(r"(?P<uuid>[\d\-a-f]+)/update", views.update),
]
