from .serializers import UserSerializer,  UserupdateSerializer
from .models import User
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
import pyotp
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class generateKey:
    @staticmethod
    def returnValue():
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=600)
        OTP = totp.now()
        return {"totp": secret, "OTP": OTP}

@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['password','email', 'full_name', 'username', 'province', 'district', 'municipality', 'ward', 'skills', 'address', 'gender', 'phone', 'facebook', 'instagram', 'twitter', 'website', 'description', 'volunteer', 'organization', 'admin', 'active', 'verify', 'reject', 'age', 'staff'],
        properties={
            'password':openapi.Schema(type=openapi.TYPE_STRING),
            'email':openapi.Schema(type=openapi.TYPE_STRING),
            'full_name':openapi.Schema(type=openapi.TYPE_STRING),
            'username':openapi.Schema(type=openapi.TYPE_STRING),
            'province':openapi.Schema(type=openapi.TYPE_STRING),
            'district':openapi.Schema(type=openapi.TYPE_STRING),
            'municipality':openapi.Schema(type=openapi.TYPE_STRING, example="Bhaktapur"),
            'ward':openapi.Schema(type=openapi.TYPE_STRING),
            'skills':openapi.Schema(type=openapi.TYPE_STRING, example="Health"),
            'address':openapi.Schema(type=openapi.TYPE_STRING),
            'gender':openapi.Schema(type=openapi.TYPE_STRING),
            'phone':openapi.Schema(type=openapi.TYPE_STRING), 
            'facebook':openapi.Schema(type=openapi.TYPE_STRING), 
            'instagram':openapi.Schema(type=openapi.TYPE_STRING), 
            'twitter':openapi.Schema(type=openapi.TYPE_STRING), 
            'website':openapi.Schema(type=openapi.TYPE_STRING), 
            'description':openapi.Schema(type=openapi.TYPE_STRING), 
            'volunteer':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True), 
            'organization':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False), 
            'admin':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False), 
            'active':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False), 
            'verify':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False), 
            'reject':openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False), 
            'age':openapi.Schema(type=openapi.TYPE_STRING), 
            'staff':openapi.Schema(type=openapi.TYPE_STRING), 
        },
    ),
)
@api_view(['POST'])
def registerUser(request):
    """
        Register a user
    """
    key = generateKey.returnValue()
    data = request.data
    
    try:
        user = User.objects.create(
            password=make_password(data['password']),
            email=data['email'],
            full_name=data['full_name'],
            username=data['username'],
            province=data['province'],
            district=data['district'],
            municipality=data['municipality'],
            ward=data['ward'],
            skills=data['skills'],
            address=data['address'],
            gender=data['gender'],
            phone=data['phone'],
            facebook=data['facebook'],
            instagram=data['instagram'],
            description=data['description'],
            volunteer=data['volunteer'],
            organization=data['organization'],
        )
        user.images = request.FILES.get('image')
        user.identity = request.FILES.get('identity')
        user.save()
    except:
        if(User.objects.get(email=data['email'])):
            if(User.objects.get(username=data['username'])):
                data = {"message": "Email and Username already exists"}
            else:
                data = {"message": "Email already exists"}
        else:
            data = {"message": "Username already exists"}

        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user, many=False)

    try:
        email_template = render_to_string('signup_otp.html', {
                                            "otp": key['OTP'], "username": serializer.data['username'], "email": serializer.data['email']})
        sign_up_msg = EmailMultiAlternatives(
            "Otp Verification",
            "Otp Verification",
            settings.EMAIL_HOST_USER,
            [serializer.data['email']],
        )

        sign_up_msg.attach_alternative(email_template, 'text/html')
        sign_up_msg.send()
        return Response({"success" : "User Registered Successfully"})
    except:
        return Response({"info" : "User Created Successfully but email not sent"})
 
@api_view(["POST"])
def RegisterVerify(request, id, otp):
    try:
        user =User.objects.get(id=id)
        otp_db = int(user.otp)
        if otp_db != otp:
            return Response(
                {"message": "Invalid otp", "error": True},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        else:
            activation_key = user.activation_key
            totp = pyotp.TOTP(activation_key, interval=600)
            verify = totp.verify(otp)

            if verify:
                user.active = True
                user.verify= True
                user.save()

                email_template = render_to_string(
                    "signup_otp_success.html", {"username": user.username}
                )
                sign_up = EmailMultiAlternatives(
                    "Account successfully activated",
                    "Account successfully activated",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                sign_up.attach_alternative(email_template, "text/html")
                sign_up.send()

                return Response(
                    {
                        "message": "Your account has been successfully activated!!",
                        "verified": True,
                    },
                )
            else:
                return Response(
                    {"message": "Given otp is expired!!", "timeout": True},
                )

    except:
        return Response(
            {
                "message": "Invalid otp OR No any inactive user found for given otp",
                "error": True,
            },
        )


@api_view(['POST'])
def Resend_otp(request, id):
    key = generateKey.returnValue()
    print(key)
    try:
        user = User.objects.get(id=id)
        user.otp = key['OTP']
        user.activation_key = key['totp']
        user.save()
        serializer = UserSerializer(user, many=False)
        email_template = render_to_string('signup_otp.html', {
                                          "otp": serializer.data['otp'], "username": serializer.data['username'], "email": serializer.data['email']})
        sign_up = EmailMultiAlternatives(
            "Otp Verification",
            "Otp Verification",
            settings.EMAIL_HOST_USER,
            [serializer.data['email']],
        )
        sign_up.attach_alternative(email_template, 'text/html')
        sign_up.send()

        return Response({
            "message": "OTP successfully sent to your email",
            "sent": True,
        })
    except User.DoesNotExist:
        return Response({
            "message": "OTP resend error occured",
            "sent": False,
        })


class UserUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserupdateSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_User_Profile(request, U_id):
    user = User.objects.get(id=U_id)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
