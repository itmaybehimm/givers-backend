from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

def user_is_organization(function):
    def wrap(request, *args, **kwargs):
        print(type(request.user))
        if request.user.organization == True:
            return function(request, *args, **kwargs)
        else:
            return Response({"error" : "You are not an organization."})
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_volunteer(function):
    def wrap(request, *args, **kwargs):
        print(type(request.user))
        if request.user.volunteer == True:
            return function(request, *args, **kwargs)
        else:
            return Response({"error" : "You are not an volunteer."})
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap