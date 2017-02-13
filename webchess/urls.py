from django.conf.urls import url

from . import views

app_name = 'game'
urlpatterns = [
    url(r'^api$', views.api),
    url(r'^$', views.index, name='index'),
]
