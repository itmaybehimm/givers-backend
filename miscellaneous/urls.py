from django.urls import path
from .import views

urlpatterns = [
     # Show events of given category id
    path('events/sort/<int:category_id>/', views.show_specific_category, name='sort_category'),
    # show events in descending order of event date
    path('events/sort_desc/', views.show_event_desc, name='show_event_desc'),
    # show events in order of posted time
    path('events/', views.show_event_postedtime, name='show_posted_latest'),
    # search the events
    path('events/search/', views.searchevents, name='search_event'),
    path('users/search/', views.searchuser, name='search_user'),
    path('show/number/<int:E_id>/',
         views.show_number_approved_requested, name='approval_no'),
    path('skills/search/<str:skill>',
         views.search_by_skills, name='search_skills'),
    path('advance_search/',
         views.advance_search.as_view(), name='advance_search'),
]
