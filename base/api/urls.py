from django.urls import path
from . import views


urlpatterns = [

    path('room/', views.rooms ),
    path('room/<int:pk>', views.room )
]