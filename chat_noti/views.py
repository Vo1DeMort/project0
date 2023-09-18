from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Room ,Message

@login_required
def all_rooms(request):
    # create a new room functionality
    # search or start a chat: if the room already exists , user will be redirect to the room

    rooms = Room.objects.filter(participants=request.user)

    rooms_dudes = []
    for room in rooms :
        other_dude = room.participants.exclude(id=request.user.id).first()
        rooms_dudes.append((room,other_dude))

    return render(request,'rooms.html',{'rooms_dudes':rooms_dudes})

def chat_room (request,room_id):
    room = get_object_or_404(Room,pk = room_id)
    # load the message of the chat

    other_dude = room.participants.exclude(id=request.user.id).first()
    return render(request,'room.html',{'room':room,'other_dude':other_dude})

