from django.forms import ValidationError

from requests import request
from .models import Events
from .serializers import EventSerializer, EventupdateSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from customuser.models import User
from category.models import EventCategory

from givers.decorators import user_is_organization

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Event_display_all(request):
    """
        Display all the events
    """
    all_events = Events.objects.all()
    serializer = EventSerializer(all_events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Event_display_id(request, E_id):
    """
        Get the event with the provided Event ID parameter
    """
    event = Events.objects.get(id=E_id)
    serializer = EventSerializer(event, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Event_display_specific(request, user_id):
    """
        Display all the INCOMPLETE events of a specific user
        Parameters Requred = ['user_id']
    """
    try:
        user = User.objects.get(id=user_id)
        event = Events.objects.filter(user=user, completed=False)
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error" : "No User Found"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Event_display_completed(request, user_id):
    """
        Display all the COMPLETED EVENTS of the specific user
    """
    try:
        user = User.objects.get(id=user_id)
        event = Events.objects.filter(user=user, completed=True)
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({"error" : "No User Found"})


@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['category','name', 'location', 'start_date', 'end_date', 'description', 'completed', 'banner'],
        properties={
            'category':openapi.Schema(type=openapi.TYPE_STRING),
            'name':openapi.Schema(type=openapi.TYPE_STRING),
            'location':openapi.Schema(type=openapi.TYPE_STRING),
            'start_date':openapi.Schema(type=openapi.TYPE_STRING, default="yyyy-mm-dd"),
            'end_date':openapi.Schema(type=openapi.TYPE_STRING, default='yyyy-mm-dd'),
            'description':openapi.Schema(type=openapi.TYPE_STRING), 
            'completed':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            'banner': openapi.Schema(type=openapi.TYPE_FILE),
        },
    ),
    operation_description='Create Events : To Create an event, you must be an organization' 
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_is_organization
def registerEvent(request):
    data = request.data
    try:
        Event = Events.objects.create(
            user = request.user,
            category=EventCategory.objects.get(category=data['category']),
            name=data['name'],
            location=data['location'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            description=data['description'],
            completed=data['completed'],
        )
        serializer = EventSerializer(Event, many=False)
        Event = Events.objects.get(id=serializer.data['id'])
        Event.banner = request.FILES.get('banner')
        Event.save()
        serializer = EventSerializer(Event, many=False)
        return Response(serializer.data)
    except ValidationError as e:
        return Response({"ValidationError" : e}, status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        message = {'error': e}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class EventUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Events.objects.all()
    serializer_class = EventupdateSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLoginUserEvents(request):
    """
        Display all the events of the currently logged in user
    """
    events = Events.objects.filter(user = request.user)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
