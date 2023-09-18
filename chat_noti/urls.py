from django.urls import path
from .import views


urlpatterns = [
    path('rooms/', views.all_rooms, name='all_rooms'),
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
]
