
# registration logic

# This file handles the registration process.
# It validates submitted form data, creates a user account and redirects to login.
# rander show html page in browser.
# redirect send user one url to another url.
# registrationform import kiya jo form.py me use kiya hai
# request give information from come browser., when user open form or summit tha form django run
# this function.
# post check user summietd tha form or not it also send the request to server.
# get open page or input data.
# form = RegistrationForm(request.POST) send data to resitrasion form.
#  RegistrationForm() if some do registrasion at first time it provide a blank form.


# This file handles user registration, login and logout.
# It manages authentication and redirects users to the correct pages.



# This file handles user registration, login and logout.
# It manages groups, members, private messages and group messages.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Group, Message, UserProfile

from .forms import (
    RegistrationForm,
    LoginForm,
    GroupForm,
    AddMemberForm,
    MessageForm
)


# Registration View

def register_view(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            mobile_number = form.cleaned_data['mobile_number']

            user = form.save()

            UserProfile.objects.create(
                user=user,
                mobile_number=mobile_number
            )

            return redirect('login')

    else:

        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


# Login View

def login_view(request):

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            return redirect('home')

    else:

        form = LoginForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


# Logout View

def logout_view(request):

    logout(request)

    return redirect('login')


# Home View

@login_required
def home_view(request):

    return render(request, 'accounts/home.html')


# Create Group View

@login_required
def create_group_view(request):

    if request.method == 'POST':

        form = GroupForm(request.POST)

        if form.is_valid():

            group = form.save(commit=False)

            group.created_by = request.user

            group.save()

            group.members.add(request.user)

            return redirect('my_groups')

    else:

        form = GroupForm()

    return render(
        request,
        'accounts/create_group.html',
        {'form': form}
    )


# My Groups View

@login_required
def my_groups_view(request):

    groups = Group.objects.filter(
        members=request.user
    ).distinct()

    return render(
        request,
        'accounts/my_groups.html',
        {'groups': groups}
    )


# Add Members View

@login_required
def add_members_view(request, group_id):

    group = get_object_or_404(
        Group,
        id=group_id,
        created_by=request.user
    )

    if request.method == 'POST':

        form = AddMemberForm(request.POST)

        if form.is_valid():

            search_query = form.cleaned_data['search_query'].strip()

            # Search user by username

            member = User.objects.filter(
                username__iexact=search_query
            ).exclude(
                id=request.user.id
            ).first()

            # If username not found, search by mobile number

            if member is None:

                profile = UserProfile.objects.select_related(
                    'user'
                ).filter(
                    mobile_number=search_query
                ).first()

                if profile:
                    member = profile.user

                    if member == request.user:
                        member = None

            # Check search result

            if member is None:

                messages.error(
                    request,
                    'No user found with this username or mobile number.'
                )

            # Check if already a group member

            elif group.members.filter(id=member.id).exists():

                messages.warning(
                    request,
                    f'{member.username} is already a member of this group.'
                )

            else:

                group.members.add(member)

                messages.success(
                    request,
                    f'{member.username} has been added to the group.'
                )

            return redirect(
                'add_members',
                group_id=group.id
            )

    else:

        form = AddMemberForm()

    return render(
        request,
        'accounts/add_members.html',
        {
            'form': form,
            'group': group
        }
    )


# Send Message View
# Supports both private and group messages

@login_required
def send_message_view(request, group_id=None, receiver_id=None):

    group = None
    receiver = None

    if group_id is not None:

        group = get_object_or_404(
            Group,
            id=group_id,
            members=request.user
        )

        chat_messages = Message.objects.filter(
            group=group
        ).order_by('created_at')

    elif receiver_id is not None:

        receiver = get_object_or_404(
            User,
            id=receiver_id
        )

        if receiver == request.user:

            return redirect('home')

        chat_messages = Message.objects.filter(
            Q(sender=request.user, receiver=receiver) |
            Q(sender=receiver, receiver=request.user),
            group__isnull=True
        ).order_by('created_at')

    else:

        return redirect('home')

    if request.method == 'POST':

        form = MessageForm(request.POST)

        if form.is_valid():

            message = form.save(commit=False)

            message.sender = request.user

            if group is not None:

                message.group = group

            else:

                message.receiver = receiver

            message.save()

            if group is not None:

                return redirect(
                    'group_messages',
                    group_id=group.id
                )

            return redirect(
                'private_messages',
                receiver_id=receiver.id
            )

    else:

        form = MessageForm()

    return render(
        request,
        'accounts/messages.html',
        {
            'form': form,
            'chat_messages': chat_messages,
            'group': group,
            'receiver': receiver
        }
    )


# Delete Group View

@login_required
@require_POST
def delete_group_view(request, group_id):

    group = get_object_or_404(
        Group,
        id=group_id,
        created_by=request.user
    )

    group.delete()

    return redirect('my_groups')


# Delete Message View

@login_required
@require_POST
def delete_message_view(request, message_id):

    message = get_object_or_404(
        Message,
        id=message_id,
        sender=request.user
    )

    group_id = message.group_id

    receiver_id = message.receiver_id

    message.delete()

    if group_id is not None:

        return redirect(
            'group_messages',
            group_id=group_id
        )

    return redirect(
        'private_messages',
        receiver_id=receiver_id
    )


# Users List View

@login_required
def users_list_view(request):

    users = User.objects.exclude(
        id=request.user.id
    ).order_by('username')

    return render(
        request,
        'accounts/users_list.html',
        {'users': users}
    )
