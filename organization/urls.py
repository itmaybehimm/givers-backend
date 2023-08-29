from django.urls import path
from .import views

urlpatterns=[
    # For the approval of the request form and to assign task
    path('approval/<int:E_id>/<int:V_id>/',views.approval,name='approval'),
    # To show the requested events with given user id and event id
    path('approval/request/<int:E_id>/<int:U_id>/',views.showrequest,name='show_request'),
    # Get all the request form for the given event id
    path('requested/<int:E_id>/',views.show_all_requested,name='all_request'),
    # Create a request form
    path('request/form/',views.requestforms,name='request_form'),
    # get request form of the given event id
    path('requested/form/<int:E_id>/',views.getrequestedform,name='request_form'),
]