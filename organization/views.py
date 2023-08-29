from customuser.serializers import UserSerializer
from events.serializers import EventSerializer
from givers.decorators import user_is_organization
from volunteer.models import requestevents
from .serializer import RequestFormSerializer, approvalSerializer, requestedSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from customuser.models import User
from events.models import Events
from .models import requestform
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showrequest(request, E_id, U_id):
    """
        Get the requestevents with given user_id(U_id) and event_id(E_id)
    """
    try:
        approval = requestevents.objects.filter(user_id=U_id, event_id=E_id)
        serializer = approvalSerializer(approval, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except requestevents.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['approved', 'task_assigned'],
        properties={
            'approved':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True, description="True to approve the request event of a volunteer"),
            'task_assigned':openapi.Schema(type=openapi.TYPE_STRING, description="If approved, then assign task.")
        },
    ),
)
@api_view(['POST'])
def approval(request, E_id, V_id):
    """
        For the approval of the Request Form for an events
        Function 1 : To approve or mark pending to a request form based on questions and answer
        Function 2 : Send email on the case if the Request form is accepted or rejected to the volunteer
    """
    print(request.data)
    try:
        approved_bool = True if request.data['approved'] == 'True' else False
        approval = requestevents.objects.get(user_id=V_id, event_id=E_id)
        approval.approved = approved_bool
        approval.pending = not(approved_bool)
        approval.task_assigned=request.data['task_assigned']
        approval.save()
        serializer = approvalSerializer(approval, many=False)
        event = Events.objects.get(id=E_id)
        user = User.objects.get(id=V_id)
        user_name = UserSerializer(user, many=False)
        eventname = EventSerializer(event, many=False)
        if(serializer.data['approved'] == True):
            email_template = render_to_string('Approved.html', {
                                              "event": eventname.data['name'], "username": user_name.data['username'],"task":serializer.data['task_assigned']})
            approved = EmailMultiAlternatives(
                "Approved",
                "Approved",
                settings.EMAIL_HOST_USER,
                [user_name.data['email']],
            )
            # approved.attach_alternative(email_template, 'text/html')
            # approved.send()
        elif(serializer.data['approved'] == False):
            email_template = render_to_string('Rejected.html', {
                                              "event": eventname.data['name'], "username": user_name.data['username']})
            rejected = EmailMultiAlternatives(
                "Rejected",
                "Rejected",
                settings.EMAIL_HOST_USER,
                [user_name.data['email']],
            )
            # rejected.attach_alternative(email_template, 'text/html')
            # rejected.send()

        return Response({"success": True})

    except requestevents.DoesNotExist:
        return Response({"success": False}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_all_requested(request, E_id):
    """
        Show all the request form of the given event id
    """
    try:
        requested = requestevents.objects.filter(
            event_id=E_id, request_volunteer=True)
        serializer = requestedSerializer(requested, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except requestevents.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['id', 'ques_1', 'ques_2', 'ques_3', 'file_1'],
        properties={
            'id':openapi.Schema(type=openapi.TYPE_INTEGER, description="Id of an event"),
            'ques_1':openapi.Schema(type=openapi.TYPE_STRING),
            'ques_2':openapi.Schema(type=openapi.TYPE_STRING),
            'ques_3':openapi.Schema(type=openapi.TYPE_STRING),
            'file_1':openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_is_organization
def requestforms(request):
    """
        Creating a request form for an organization
    """
    data = request.data
    try:
        form = requestform.objects.create(
            event=Events.objects.get(id=data['id']),
            ques_1=data['ques_1'],
            ques_2=data['ques_2'],
            ques_3=data['ques_3'],
            file_1=data['file_1'],
        )
        serializer = RequestFormSerializer(form, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'you have already updated the form'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getrequestedform(request, E_id):
    """
        Get the request form the given event id
    """
    try:
        requestedform = requestform.objects.get(event_id=E_id)
        serializer = RequestFormSerializer(requestedform, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except requestevents.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)