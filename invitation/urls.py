from django.urls import path
from .import views


urlpatterns = [
    # Create an invitation
    path('<int:U_id>/<int:E_id>/', views.invite, name='invite'),
    # Get all invitation of specific user
    path('<int:U_id>/', views.invite_display_id, name='invitation'),
    # Mark Read to the read invitations
    path('read/<int:I_id>/',
         views.invite_display_id_read, name='invitation_read'),
]
