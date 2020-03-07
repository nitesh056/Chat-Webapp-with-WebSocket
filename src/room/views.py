from django.shortcuts import render, redirect
from .models import Room, Message, UserJoined

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

    if UserJoined.objects.filter(user=request.user, room=room).count() == 0:
        UserJoined.objects.create(user=request.user, room=room, status='ONLINE')
    
    userStatus = UserJoined.objects.get(user=request.user, room=room)
    userStatus.status = 'ONLINE'
    userStatus.save()

    online_users = UserJoined.objects.filter(room=room, status='ONLINE')
    offline_users = UserJoined.objects.filter(room=room, status='OFFLINE')

    context_variables = {
        'chat_messages': messages,
        'room': room,
        'online_users': online_users,
        'offline_users': offline_users
    }

    return render(request, 'message_room.html', context_variables)
