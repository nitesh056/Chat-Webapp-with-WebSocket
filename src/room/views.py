from django.shortcuts import render, redirect
from .models import Room, Message

def view_rooms(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        context_variables = {
            'rooms' : rooms
        }
        return render(request, 'rooms.html', context_variables)

    if request.method == 'POST':
        room = Room.objects.create(room_name=request.POST['room_name'])
        return redirect('/rooms/')

def message_room(request, id):
    room = Room.objects.get(id=id)
    messages = Message.objects.filter(room=room)
    context_variables = {
        'chat_messages' : messages,
        'room' : room
    }

    return render(request, 'message_room.html', context_variables)
