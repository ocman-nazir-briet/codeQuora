from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from .forms import *  
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def loginUser(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Invalid Username')
        user = authenticate(request, username=username, password=password)
        print(username)
        print(password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in Successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Password')
    return render(request, 'base/login.html')
            

def logoutUser(request):
    logout(request)
    return render(request, 'base/login.html')

@login_required(login_url='/login')
def index(request):
    topic = Topic.objects.all()
    q = request.GET.get('q') if request.GET.get('q')  != None else ''
    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count=room.count()

    return render(request, 'base/home.html', {'room':room, 'topic':topic, 'room_count':room_count})

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    return render(request, 'base/createRoom.html', {'form':form})

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/room.html', {'form':form})

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('/')
    return render(request, 'base/delete.html', {'room':room})