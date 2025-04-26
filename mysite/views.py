from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from .models import Community
from .forms import CommunityForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import CommentForm 
from .models import Comment


#Explore
@login_required
def explore(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('explore')
    else:
        form = PostForm(user=request.user)

    joined_communities = request.user.joined_communities.all()
    posts = Post.objects.filter(community__in=joined_communities).order_by('-timestamp')

    return render(request, 'explore.html', {
        'form': form,
        'posts': posts,
        'joined_communities': joined_communities
    })

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user == request.user:
        post.delete()
    
    return redirect('explore')
    
@login_required
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({'liked': liked, 'like_count': post.total_likes()})

def events(request):
    return render(request, 'mysite/events.html')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None).order_by('-timestamp')  
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                new_comment.parent_id = int(parent_id)
            new_comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })
    
def reply_to_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.parent = parent_comment
            reply.save()
            return redirect('post_detail', post_id=post.id)

    return redirect('post_detail', post_id=post.id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.text = 'post deleted'
        comment.deleted = True
        comment.save()
    return redirect('post_detail', post_id=comment.post.id)

# My Community
def mycommunity(request):
    user = request.user
    owned = Community.objects.filter(created_by=user)
    joined = user.joined_communities.all()
    suggested = Community.objects.exclude(id__in=joined).exclude(created_by=user)
    return render(request, 'mysite/mycommunity.html', {
        'owned_communities': owned,
        'joined_communities': joined,
        'suggested_communities': suggested,
    })
    
def create_community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user
            community.save()
            community.members.add(request.user)  
            return redirect('mycommunity')
    else:
        form = CommunityForm()
    return render(request, 'create_community.html', {'form': form})


def toggle_community_membership(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    
    if request.user in community.members.all():
        community.members.remove(request.user)
    else:
        community.members.add(request.user)

    return redirect('mycommunity')

def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    posts = community.posts.select_related('user').all().order_by('-timestamp') 

    return render(request, 'mysite/community_detail.html', {
        'community': community,
        'posts': posts,
    })

@login_required
def delete_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    # Only allow deleting if the current user made the community
    if request.user == community.created_by:
        community.delete()
    
    return redirect('mycommunity')