
# This file manages URLs for the accounts app.
# It connects the registration URL with its view function.
# path to make url.
# views to access views.py of this function.
# views.register_view tell us which function run when open url.
#  name='register' url ko pehchanne ke liye.

# This file manages registration, login, logout and home URLs.
# It connects URLs with their view functions.




from django.urls import path
from . import views


urlpatterns = [

    # Welcome Page
    path('', views.welcome_view, name='welcome'),

    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),

    # Group URLs
    path(
        'create-group/',
        views.create_group_view,
        name='create_group'
    ),

    path(
        'my-groups/',
        views.my_groups_view,
        name='my_groups'
    ),

    path(
        'add-members/<int:group_id>/',
        views.add_members_view,
        name='add_members'
    ),

    # Messaging URLs
    path(
        'users/',
        views.users_list_view,
        name='users_list'
    ),

    path(
        'group-messages/<int:group_id>/',
        views.send_message_view,
        {'receiver_id': None},
        name='group_messages'
    ),

    path(
        'private-messages/<int:receiver_id>/',
        views.send_message_view,
        {'group_id': None},
        name='private_messages'
    ),

    # Delete URLs
    path(
        'delete-group/<int:group_id>/',
        views.delete_group_view,
        name='delete_group'
    ),

    path(
        'delete-message/<int:message_id>/',
        views.delete_message_view,
        name='delete_message'
    ),

]
