from django.urls import path
from .views import index, single_station, daterange, battery, tongji, jtest
urlpatterns = [
    path('', index),
    path('singlestation/<str:station_num>', single_station),
    path('singlestation/<str:station_num>/intimes/<str:start>/<str:end>', single_station),
    path('daterange', daterange),
    path('battery', battery),
    path('tongji', tongji),
    path('jtest', jtest)
]