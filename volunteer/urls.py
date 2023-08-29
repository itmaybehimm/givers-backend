from django.urls import path
from .import views

urlpatterns = [
    # Create a request event by volunteer for an event
    path('request_event/<int:U_id>/<int:E_id>/',
         views.request_event, name='request_event'),
    # Show all the events that the user is interested
    path('interested/<int:U_id>/', views.showinterested, name='interested'),
    # Create an interestEvent modal 
    path('interested/event/', views.interestedevent, name='interested_event'),
    path('get_request_event/<int:U_id>/<int:E_id>',views.requestevent),
    path('requested_specific/<int:U_id>/', views.show_requested_specific_user, name='requested_specific_user'),
]
