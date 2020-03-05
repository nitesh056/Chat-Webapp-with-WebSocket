from django.urls import path
from .views import *

urlpatterns = [
    path('', view_rooms),
    path('<int:id>', message_room)
]
