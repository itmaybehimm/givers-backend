from .models import interestedevents, requestevents
from .serializers import interestedSerializervolunteer, requesteventSerializervolunteer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from customuser.models import User
from events.models import Events

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['ques_1', 'ques_2', 'ques_3', 'ans_1', 'ans_2', 'ans_3', 'request_volunteer', 'approved', 'file_1'],
        properties={
            'ques_1':openapi.Schema(type=openapi.TYPE_STRING),
            'ques_2':openapi.Schema(type=openapi.TYPE_STRING),
            'ques_3':openapi.Schema(type=openapi.TYPE_STRING),
            'ans_1':openapi.Schema(type=openapi.TYPE_STRING),
            'ans_2':openapi.Schema(type=openapi.TYPE_STRING),
            'ans_3':openapi.Schema(type=openapi.TYPE_STRING),
            'request_volunteer':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True),
            'approved':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
            'file_1':openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def request_event(request, U_id, E_id):
    """
        Make a request for volunteer to the event(with id = E_id) by user(U_id)
    """
    if requestevents.objects.filter(user_id=U_id, event_id=E_id).exists():
        message = {"message": "You have already requested to this event"}
        return Response(message)
    else:
        data = request.data
        try:
            approved_bool = True if data["approved"] == True else False
            requestevent = requestevents.objects.create(
                user=User.objects.get(id=U_id),
                event=Events.objects.get(id=E_id),
                # description=data['description'],
                ques_1=data["ques_1"],
                ques_2=data["ques_2"],
                ques_3=data["ques_3"],
                ans_1=data["ans_1"],
                ans_2=data["ans_2"],
                ans_3=data["ans_3"],
                request_volunteer=data["request_volunteer"],
                approved=approved_bool,
                pending=not(approved_bool),
                file_1=data["file_1"],
                task_assigned=False,
            )
            serializer = requesteventSerializervolunteer(requestevent, many=False)
            requestevent = requestevents.objects.get(id=serializer.data["id"])
            requestevent.user_details = request.FILES.get("user_details")
            requestevent.save()
            serializer = requesteventSerializervolunteer(requestevent, many=False)

            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def showinterested(request, U_id):
    """
        Show all the events that the user is interested
    """
    try:
        interested = interestedevents.objects.filter(user_id=U_id, interested=True)
        serializer = interestedSerializervolunteer(interested, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except requestevents.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'name'],
        properties={
            'username':openapi.Schema(type=openapi.TYPE_STRING, description="username of  a user"),
            'name':openapi.Schema(type=openapi.TYPE_STRING, description="name of an event"),
        },
    ),
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def interestedevent(request):
    """
        Post data to show and interest in an event by the currently logged in user
    """
    data = request.data
    try:
        interested = interestedevents.objects.create(
            user=User.objects.get(username=data["username"]),
            event=Events.objects.get(name=data["name"]),
            interested=data["interested"],
        )
        serializer = requesteventSerializervolunteer(interested, many=False)
        return Response(serializer.data)
    except:
        message = {"detail": "You are already interested in this Event"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def show_requested_specific_user(request, U_id):
    """
        Show all the events that the user has applied for the volunteering
    """
    try:
        requested = requestevents.objects.filter(
            user_id=U_id, request_volunteer=True
        )
        serializer = interestedSerializervolunteer(requested, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except requestevents.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def requestevent(request,U_id,E_id):
    try:
        requested = requestevents.objects.filter(
            event_id=E_id,user_id=U_id)
        serializer = requesteventSerializervolunteer(requested,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except requestevents.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)