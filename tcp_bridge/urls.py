from django.conf.urls import url
from . import views

urlpatterns = [
    #Web Pages
    url(r'^$', views.index, name='index'),
    #REST API
	url(r'^api/$', views.api, name='api'),
]
