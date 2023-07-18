from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follow, Like


def index(request):

    if request.method == "POST":
        if not request.POST["post-user"]:
            return HttpResponseRedirect(reverse("login"))
        else:
            comment = request.POST["post"]
            author = request.POST["post-user"]
            author = User.objects.get(id=author)
            Post.objects.create(comment=comment, author=author).save()

    posts = Post.objects.all().order_by('-timestamp')
    posts_paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_page_object = posts_paginator.get_page(page_number)

    likes = Like.objects.all()
    postsYouLike = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                postsYouLike.append(like.post.id)        
    except:
        postsYouLike= []

    return render(request, "network/index.html", {
        "postsYouLike": postsYouLike,
        "postsPage": posts_page_object
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, id):
    
    user_profile = User.objects.get(id=id)
    posts = Post.objects.filter(author=user_profile).order_by('-timestamp')
    posts_paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_page_object = posts_paginator.get_page(page_number)

    following_count = Follow.objects.filter(followed_user=id).count()
    followers_count = Follow.objects.filter(follower=id).count()

    isFollowing = Follow.objects.filter(followed_user=user_profile, follower=request.user).exists()

    likes = Like.objects.all()
    postsYouLike = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                postsYouLike.append(like.post.id)       
    except:
        postsYouLike= []

    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "follower": followers_count,
        "following": following_count,
        "isFollowing": isFollowing,
        "postsYouLike": postsYouLike,
        "postsPage": posts_page_object,
        })


def following(request):

    user = User.objects.get(id=request.user.id)
    
    # Get the list of users followed by the signed-in user
    followed_users = Follow.objects.filter(follower=user).values_list('followed_user', flat=True)
    # Filter posts made by the followed users
    posts = Post.objects.filter(author__in=followed_users).order_by('-timestamp')
    posts_paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_page_object = posts_paginator.get_page(page_number)

    likes = Like.objects.all()
    postsYouLike = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                postsYouLike.append(like.post.id)      
    except:
        postsYouLike= []

    return render(request, "network/following.html", {
        "postsYouLike": postsYouLike,
        "postsPage": posts_page_object,
        })    
    


def follow(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        user = User.objects.get(pk=user_id)
        
        Follow.objects.create(followed_user=user, follower=request.user)
        
        return HttpResponseRedirect(reverse("profile", args=(user.id,)))

        


def unfollow(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        user = User.objects.get(pk=user_id)

        Follow.objects.filter(followed_user=user, follower=request.user).delete()

        return HttpResponseRedirect(reverse("profile", args=(user.id,)))
                                            

@csrf_exempt
def updatePost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        comment = data.get("comment")
        post_id = data.get("post_id")
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)

        post.comment = comment
        post.save()
        
    return JsonResponse({"success": "its working properly", "comment": post.comment})

@csrf_exempt
def removePostLike(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(pk=post_id)
 
        try:
            like = Like.objects.get(post_id=post)
            like.delete()
            like_count = Like.objects.filter(post=post).count()
            return JsonResponse({"success": "like deleted seccessfully", "like_count": like_count})
        except Like.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        
@csrf_exempt
def addPostLike(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")
        post = Post.objects.get(pk=post_id)

        like = Like.objects.create(post=post, user=request.user)
        like.save()

        like_count = Like.objects.filter(post=post).count()

    return JsonResponse({"success": "like added seccessfully", "like_count": like_count})
     