from django import views
from base.models import Room
from .serializers import RoomSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET','POST'])
def rooms(request):
    
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
def room(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    

    if request.method == 'PUT':
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    if request.method == 'DELETE':
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)