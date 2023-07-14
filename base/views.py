from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User, Topic, Room, Message
from .forms import RoomForm, RegisterForm, MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q





def home(request):
  
    rooms = Room.objects.all
    messages = Message.objects.all

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
      Q(topic__name__icontains=q) |
      Q(name__icontains=q) |
      Q(description__icontains=q)
      )
   
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()


    context = {'topics': topics, 'rooms': rooms, 'messages': messages, 'room_count':room_count}
    return render(request, 'base/home.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room':room, 'messages': messages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
           host = request.user ,
           name = request.POST.get('name'),
           topic = topic,
           description = request.POST.get('description')
       )
        return redirect('home')

    return render(request, 'base/create-room.html', {'topics':topics ,'form': form } )
    



def updateRoom(request, pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
      
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
   
        room.name = request.POST.get('name')
        room.topic = topic
        room.host = request.user
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    return render(request, 'base/create-room.html' , {'form': form, 'room': room, 'topics':topics })




def activityPage(request):
    messages = Message.objects.all()
    context = {'messages': messages}
    return render(request, 'base/activity_component.html', context )


def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            return HttpResponse( 'User does not exist')


        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Username or Password does not exist!')
    
    return render(request, 'base/login.html')


def logoutPage(request):
    logout(request)
    return redirect('home')



def register(request):
    form = MyUserCreationForm()
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('There was an error during registeration')
    return render(request, 'base/register.html', {'form': form})



def deleteMessage(request, pk):
    obj = Message.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': obj})




def deleteRoom(request, pk):
    obj = Room.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': obj})



def profile(request, pk):
    topics = Topic.objects.all
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    messages = user.message_set.all()
    room_count = rooms.count

    context = {'topics': topics, 'rooms': rooms, 'messages': messages, 'user':user , 'room_count':room_count}
    return render(request, 'base/profile.html', context)



def editUser(request):
    user = request.user
    form = RegisterForm(instance=user)

    if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES, instance=user)
            form.avatar = request.POST.get('avatar')
            user = form.save(commit=False)
            user.save()
            
            return redirect('profile', user.id)
    
    return render(request,  'base/edit-user.html',{'form': form})
    


def activity(request):
    messages = Message.objects.all

    context = {'messages': messages}
    return render(request, 'base/activity.html', context)



def topic(request):
    topics = Topic.objects.all
    rooms = Room.objects.all

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
      Q(topic__name__icontains=q) |
      Q(name__icontains=q) |
      Q(description__icontains=q)
      )
   
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))


    context = {'topics': topics, 'rooms': rooms}
    return render(request, 'base/topics.html', context)



#  python manage.py runserver

# ethielb47@gmail.com

# password

#  {% extends 'main.html' %} {% block content %} {% endblock %}

#  sRun7SzSNK4uKmc       uJTxAVqTY69KfGx