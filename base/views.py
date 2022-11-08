from django.shortcuts import render, redirect
from .models import *
from .forms import *  

def index(request):
    topic = Topic.objects.all()
    q = request.GET.get('q') if request.GET.get('q')  != None else ''
    room = Room.objects.filter(topic__name__icontains=q)

    return render(request, 'base/home.html', {'room':room, 'topic':topic})

def createRoom(request):
    form = RoomForm
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    return render(request, 'base/createRoom.html', {'form':form})

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/room.html', {'form':form})

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('/')
    return render(request, 'base/delete.html', {'room':room})