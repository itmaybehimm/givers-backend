from django.urls import path
from .import views

urlpatterns = [
     # For listing all events in ascending order of date
    path('events_ascending/', views.Event_display_all, name='all_events'),
    # For Displaying Event of ceratin id
    path('<int:E_id>/', views.Event_display_id, name='events_id'),
    # display the incomplete events of specific user, here user_id
    path('user/<int:user_id>/', views.Event_display_specific, name='events_specific'),
    # diplay the completed events of the specific user
    path('history/<int:user_id>/', views.Event_display_completed, name='events_history'),
    # To Register a event
    path('register/', views.registerEvent, name='register_events'),
    # To update a event
    path('update/<int:pk>/', views.EventUpdate.as_view(), name='update_events'),
    # Display all the events of the current login user
    path('self/', views.getLoginUserEvents, name="display all login user events")
]
