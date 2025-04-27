from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Profile
from .forms import ProfileSearchForm
from django.shortcuts import render, redirect, get_object_or_404
import sys
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Follow
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import User, Profile, Follow
from .forms import CustomUserCreationForm
from .models import Follow, Notification
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthForm
from .forms import CustomUserCreationForm
from accounts.models import Notification
from mysite.models import Post, Comment, Community

# Create your views here.


# ------------------------------------------REGISTER------------------------------------------------------------------------------------

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            print(f"User {user.username} created")
            return redirect('explore')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# ----------------------------------------LOGIN------------------------------------------------------------------------------------

def login(request):
    if request.method == 'POST':
        print("POST request received")
        form = CustomAuthForm(data=request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.get_user()
            auth_login(request, user)
            return redirect('explore')
        else:
            print("Form is not valid")
    else:
        form = CustomAuthForm()
        print("GET request, serving login form")
    
    return render(request, 'accounts/login.html', {'form': form})

#---------------------------------------------------- Profile ------------------------------------------------------------------------

@login_required    
def profile_view(request):
    profile = Profile.objects.get(user=request.user)  
    followers_count = request.user.followers.filter(status='F').count()
    following_count = request.user.following.filter(status='F').count()

    user_posts = Post.objects.filter(user=request.user).order_by('-timestamp')
    user_comments = Comment.objects.filter(user=request.user).order_by('-timestamp')
    joined_communities = Community.objects.filter(members=request.user)

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'user_posts': user_posts,
        'user_comments': user_comments,
        'joined_communities': joined_communities,  
    })
    

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)  
        if form.is_valid():
            profile = form.save(commit=False)  
            profile.save()                     
            form.save_m2m()                    
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
        
    return render(request, 'accounts/editprofile.html', {'form': form})


@login_required    
def search_profiles(request):
    form = ProfileSearchForm(request.GET or None)
    profiles = None  
    
    if request.GET and form.is_valid():
        search_term = form.cleaned_data['search_term']
        print(f"Search term received: {search_term}")  

        profiles = Profile.objects.filter(user__username__icontains=search_term)
        # exclude the current user's profile from results
        profiles = profiles.exclude(user=request.user)

        print(f"Found {profiles.count()} profiles matching the search term.")  
    
    if not profiles:
        print("No profiles found.")  
    
    return render(request, 'accounts/search.html', {'form': form, 'profiles': profiles})

@login_required
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    followers_count = user.followers.filter(status='F').count()
    following_count = user.following.filter(status='F').count()
    is_following = Follow.objects.filter(follower=request.user, followee=user, status=Follow.FOLLOWING).exists()
    follow_request_sent = Follow.objects.filter(follower=request.user, followee=user, status=Follow.PENDING).exists()

    user_posts = Post.objects.filter(user=user).order_by('-timestamp')
    user_comments = Comment.objects.filter(user=user).order_by('-timestamp')
    joined_communities = Community.objects.filter(members=user)

    if profile.is_public or is_following:
        return render(request, 'accounts/profile_detail.html', {
            'profile': profile,
            'followers_count': followers_count,
            'following_count': following_count,
            'user_posts': user_posts,
            'user_comments': user_comments,
            'joined_communities': joined_communities,
            'is_following': is_following
        })
    else:
        return render(request, 'accounts/profile_private.html', {
            'profile': profile,
            'follow_request_sent': follow_request_sent
        })

    
@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_to_follow)

    follow_instance, created = Follow.objects.get_or_create(follower=request.user, followee=user_to_follow)

    if profile.is_public:
        follow_instance.status = Follow.FOLLOWING
        follow_instance.save()
        
        
        Notification.objects.get_or_create(
            to_user=user_to_follow,
            from_user=request.user,
            notification_type='F',  
            defaults={'message': f'{request.user.username} started following you.'}
        )

        messages.success(request, f'You are now following {user_to_follow.username}.')
    
    else:
        if created or follow_instance.status != Follow.PENDING:
            follow_instance.status = Follow.PENDING
            follow_instance.save()

            Notification.objects.get_or_create(
                to_user=user_to_follow,
                from_user=request.user,
                notification_type='FR',
                defaults={'message': f'{request.user.username} has requested to follow you.'}
            )

            messages.success(request, f'Follow request sent to {user_to_follow.username}.')
        else:
            messages.info(request, f'Follow request already sent to {user_to_follow.username}.')

    return redirect('accounts:profile_detail', username=username)


@login_required
def revoke_follow_request(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    follow_instance = get_object_or_404(Follow, follower=request.user, followee=user_to_unfollow, status=Follow.PENDING)
    follow_instance.delete()

    Notification.objects.filter(to_user=user_to_unfollow, from_user=request.user, notification_type=Notification.FOLLOW_REQUEST).delete()

    messages.success(request, f'Follow request to {user_to_unfollow.username} has been revoked.')
    return redirect('accounts:profile_detail', username=username)

@login_required
def unfollow(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, followee=user_to_unfollow).delete()
    return redirect('accounts:profile_detail', username=username)

@login_required
def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers_profiles = Profile.objects.filter(user__in=user.followers.values_list('follower', flat=True))
    print(f"User: {user.username} is followed by: {followers_profiles.count()} users.")
    return render(request, 'accounts/followers_list.html', {'user': user, 'profiles': followers_profiles})

@login_required
def following_list(request, username):
    user = get_object_or_404(User, username=username)
    
    following_profiles = Profile.objects.filter(user__followers__follower=user, user__followers__status=Follow.FOLLOWING)
    print(f"User: {user.username} follows: {following_profiles.count()} users.")
    return render(request, 'accounts/following_list.html', {'user': user, 'profiles': following_profiles})

@login_required
def notifications(request):
    user_notifications = request.user.notifications_to.all()  
    
    user_notifications.update(is_read=True)
    return render(request, 'accounts/notifications.html', {'notifications': user_notifications})

@login_required
def accept_follow_request(request, notification_id):
    
    notification = get_object_or_404(Notification, id=notification_id, to_user=request.user)
    follow, created = Follow.objects.get_or_create(follower=notification.from_user, followee=request.user)

    
    follow.status = Follow.FOLLOWING
    follow.save()

    Notification.objects.create(
        to_user=notification.from_user,
        from_user=request.user,
        notification_type=Notification.FOLLOW_ACCEPTED,
        message=f"{request.user.username} has accepted your follow request."
    )

    
    notification.delete()

    return redirect('accounts:notifications')

@login_required
def reject_follow_request(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, to_user=request.user)
    follow = Follow.objects.filter(follower=notification.from_user, followee=request.user, status=Follow.PENDING)
    follow.delete()
    notification.delete()  
    return redirect('accounts:notifications')