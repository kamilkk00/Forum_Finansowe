from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, reverse, redirect
from .models import User, Post, Comment, ProfessionalUser, Save_Post, Like, Like_Comment, Rating_User
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown2
from django.utils.safestring import mark_safe

# Creating the main page with posts in descending order of likes
def index(request):
    post = Post.objects.all().order_by('-like_count')

    paginator = Paginator(post, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render (request, "finance/index.html",{
        "posts": posts,
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'finance/login.html',{
                "message": "Nieprawidłowa nazwa użytkownika lub hasło."
            })
    else: 
        return render (request,"finance/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "finance/register.hmtl",{
                "message": "Hasła muszą się zgadzać."
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "finance/register.html",{
                "message": "Nazwa użytkownika jest już zajęta."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"finance/register.html")

# Creating new post
def create(request):
    user = request.user if request.user.is_authenticated else None
    timestamp = datetime.now()
    categories = dict(Post.CATEGORY_CHOICES)

    if request.method == "POST":
        temat = request.POST["subject"]
        post = request.POST["content"]
        category = request.POST["category"]
        post = Post.objects.create(user=user, temat=temat, post=post, timestamp=timestamp, category=category)
        return render(request, "finance/create.html",{
            "message": "Twój artykuł został pomyślnie utworzony.",
            "categories": categories
        })

    return render(request, "finance/create.html",{
        "categories": categories
    })

# Displaying user profile along with published posts
def profile(request, user_username):
    username = user_username
    
    try:
        profile_user = User.objects.get(username=username)
        user_exist = True
    except User.DoesNotExist:
        profile_user = None

    if profile_user:
        posts = Post.objects.filter(user=profile_user)
    else:
        posts = []

    # Checking if that user exist in databases 
    user_exist = False
    users = User.objects.all()
    for user in users:
        if username == user.username:
            user_exist = True

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)


    return render(request, "finance/profile.html",{
        "username": username,
        "user_exist": user_exist,
        "profile_user": profile_user,
        "posts": posts
    })

# Displaying a single post, along with comments
def post_page(request, post_id):

    user = request.user
    that_post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post_id = post_id)
    post_saved = 1
    if user.is_authenticated: 
        try: 
            post_saved = Save_Post.objects.get(post_id = post_id, user = request.user )
        except Save_Post.DoesNotExist:
            post_saved = None

        liked_comments = Like_Comment.objects.filter(user= request.user, if_like=True).values_list('comment_id', flat=True)
    else:
        liked_comments= []

    # Creating comment
    if request.method == "POST":
        comment_text = request.POST.get('comment')
        if comment_text:
            new_comment = Comment(
                user = request.user,
                post = that_post,
                comment = comment_text
            )
            new_comment.save()
            return redirect('post_page', post_id=post_id)
        
    # Likes 
    if user.is_authenticated:
        likes = Like.objects.filter(post_id = post_id, user = request.user)
    else:
        likes = []

    post_content_markdown = markdown2.markdown(that_post.post)

    return render(request, "finance/post_page.html",{
        "post":that_post,
        "comments": comments,
        "saved": post_saved,
        "likes": likes,
        "liked_comments": liked_comments,
        "post_content_markdown": post_content_markdown
    })

# Upgrading user to professional
@login_required
def create_professional(request):

    if request.method == "POST": 
        company_name = request.POST.get("companyName")
        city = request.POST.get("city")
        specialization = request.POST.get("specialization")
        description = request.POST.get("description")
        hourly_rate = request.POST.get("hourlyRate")
        availability = request.POST.get("availability")
        email = request.POST.get("email")
        website = request.POST.get("website")
        social_media = request.POST.get("socialMedia")
        years_of_experience = request.POST.get("experience")
        certifications = request.POST.get("certifications")

        professional_user = ProfessionalUser.objects.create(
            user = request.user,
            company_name = company_name,
            city = city,
            specialization = specialization,
            description = description,
            hourly_rate = hourly_rate,
            availability = availability,
            email = email,
            website = website,
            social_media = social_media,
            years_of_experience = years_of_experience,
            certifications = certifications
        )

        request.user.if_professional = True
        request.user.save()
        
        return redirect('professional_profile', username=request.user.username)

    return render(request,"finance/create_professional.html")

# Displaying possible categories to choose from
def categories(request):
    categories = dict(Post.CATEGORY_CHOICES)
    return render(request,"finance/categories.html",{
        "categories": categories
    })

# Displaying all posts in a given category
def category(request, post_category):
    post = Post.objects.filter(category=post_category)
    category = post_category

    paginator = Paginator(post, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)


    return render(request, "finance/post_category.html",{
        "posts": posts,
        "category": category 
    })

# Displaying professional profile along with reviews
def professional_profile(request, username):
    profile = ProfessionalUser.objects.filter(user__username = username).first()
    if profile is None:
        return render(request, "finance/profile_professional.html")
    reviews = Rating_User.objects.filter(professional_user = profile)
    average_value = reviews.aggregate(Avg('value'))['value__avg']
    return render(request, "finance/profile_professional.html",{
        "profile": profile,
        "reviews": reviews,
        "rating": average_value
    })

# Searching for posts by subject (like)
def search_subject(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(Q(temat__icontains = query))
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)


    return render(request, "finance/search.html",{
        "posts": posts,
        "query": query
    })

# Searching for posts by content (like)
def search_content(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(Q(post__icontains=query))

    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, "finance/search.html",{
        "posts": posts,
        "query": query 
    })

# All saved posts (for JSON)
def saved_post_all_detail(request):
    data = list(Save_Post.objects.values())
    return JsonResponse(data, safe=False)

# All saved posts for a given user (for JSON)
def saved_post_id(request, post_id):
    posts = Save_Post.objects.filter(post_id=post_id)
    data = []
    for saved_post in posts:
        data.append({
            "user": saved_post.user.username,
            "post": post_id,
            "if_saved": saved_post.if_save
        })
    return JsonResponse(data, safe=False)

# Saving a post using JSON
@csrf_exempt
def save_post_detail(request, post_id):
    if request.method in ['POST', 'PUT']:
        data = json.loads(request.body)
        username = data.get('username')
        if_save = data.get('if_save')

        user = User.objects.get(username=username)
        post = Post.objects.get(id = post_id)

        if request.method == 'POST':
            save_post, created = Save_Post.objects.get_or_create(user=user, post=post, defaults={'if_save': if_save})
            if created: 
                return JsonResponse({"message:" "Post został zapisany"}, status=201)
            else:
                return JsonResponse({"error": "Przedstawiony post był ju zapisany"})

        elif request.method == 'PUT':
            save_post = Save_Post.objects.get(user=user, post=post)
            save_post.if_save = if_save
            save_post.save()
            return JsonResponse({"message": "Status zapisania został zaktualizowany"}, status=200)
    else: 
        return JsonResponse({"error": "Invalid request method."}, status=405)

# Liking a post using JSON
@csrf_exempt
def like_function(request, post_id):
    if request.method in ['POST', 'PUT']:
        data = json.loads(request.body)
        username = data.get('username')
        if_like = data.get('if_like')

        user = User.objects.get(username=username)
        post = Post.objects.get(id = post_id)

        if request.method == 'POST':
            save_post, created = Like.objects.get_or_create(user=user, post=post, defaults={'if_like': if_like})
            if created: 
                return JsonResponse({"message:" "Nowy like został stwrzony"}, status=201)
            else:
                return JsonResponse({"error": "Like juz istniał"})

        elif request.method == 'PUT':
            save_post = Like.objects.get(user=user, post=post)
            save_post.if_like = if_like
            save_post.save()
            return JsonResponse({"message": "Status lika został zmieniony"}, status=200)
    else: 
        return JsonResponse({"error": "Invalid request method."}, status=405)


# View with saved posts for a given user
def view_saved_posts(request, user_username):
    user = request.user
    saved_post = Save_Post.objects.filter(user= user, if_save = True)
    post_ids = saved_post.values_list('post_id', flat=True)
    posts = Post.objects.filter(id__in = post_ids)
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)


    return render (request, "finance/saved.html",{
        "posts": posts
    } )

# View with liked posts in JSON format
def detail_like_post(request, post_id):
    like = Like.objects.filter(post_id = post_id)
    data = []
    for save_like in like:
        data.append({
            "user": save_like.user.username,
            "post": post_id,
            "if_like": save_like.if_like
        })
    return JsonResponse(data, safe=False)

# View with liked comment in JSON format
def detail_like_comment(request, comment_id):
    like_comment = Like_Comment.objects.filter(comment_id = comment_id)
    data = []
    for like_comment_add in like_comment:
        data.append({
            'user': like_comment_add.user.username,
            'comment': comment_id,
            'if_like': like_comment_add.if_like
        }) 
    return JsonResponse(data, safe=False)

# Adding a like to a comment using JSON
@csrf_exempt
def add_like_comment(request,comment_id):
    if request.method in ['POST', 'PUT']:
        data = json.loads(request.body)
        username = data.get('username')
        if_like = data.get('if_like')

        user = User.objects.get(username= username)
        comment = Comment.objects.get(id = comment_id)

        if request.method == "POST":
            save_comment_like, created = Like_Comment.objects.get_or_create(user=user, comment=comment, defaults={'if_like': if_like})
            if created: 
                return JsonResponse({"message": "New like for comment has been created"}, status=201)
            else:
                return JsonResponse({"error": "Like for this comment already exists"})

        elif request.method == 'PUT':
            save_comment_like = Like_Comment.objects.get(user=user, comment=comment)
            save_comment_like.if_like = if_like
            save_comment_like.save()
            return JsonResponse({"message": "Like comment updated"}, status=200)

    else: 
        return JsonResponse({'error': 'Invalid request method.'}, status = 405)

# Editing a post using JSON
@csrf_exempt
def edit_post(request, post_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        content = data.get("content")
        user = request.user 
        try:
            post = Post.objects.get(id = post_id)
            if post.user != user:
                return JsonResponse({"error": "Permission denied."}, status=403)
            post.post = content 
            post.save()
            return JsonResponse({"message": "Content of post has been changed correctly"}, status = 200)
        except Post.DoesNotExist:
            return JsonResponse({"eror":"Post not found"}, status=404)
    return JsonResponse({"error":"Inavelid request method."}, status = 405)

# Editing a comment using JSON
@csrf_exempt
def edit_comment(request, comment_id):
    if request.method == "PUT": 
        data = json.loads(request.body)
        content = data.get("content")
        user = request.user 
        comment = Comment.objects.get(id = comment_id)
        try:
            if comment.user != user:
                return JsonResponse({"error": "Permission denied"}, status=403)
            comment.comment = content 
            comment.save()
            return JsonResponse({"message": "Content of comment has been changed correctly"}, status = 200)
        except Comment.DoesNotExist:
            return JsonResponse({"error": "Comment not found"}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=405)

# Adding an opinion in a professional profile
def add_opinion(request, username):
    user = request.user.username

    if user == username:
        return HttpResponse("You cannot give opinion to yourself")
    elif Rating_User.objects.filter(reviewer__username = user, professional_user__user__username = username).exists():
        opinion = Rating_User.objects.filter(reviewer__username = user, professional_user__user__username = username)
        return render (request, 'finance/add_opinion.html',{
            "opinion": opinion,
        })
        
    else:
        if request.method == "POST":
            reviewer = User.objects.get(username = user)
            professional_user =  ProfessionalUser.objects.get(user__username = username)
            value = request.POST["value"]
            opinion = request.POST["opinion"]
            if_used = 'if_used' in request.POST

            Rating_User.objects.create(
                reviewer = reviewer,
                professional_user = professional_user,
                value = value,
                opinion = opinion, 
                if_used = if_used
            )
            opinion = Rating_User.objects.filter(reviewer__username = user, professional_user__user__username = username)

            message = "Opinia została dodana z sukcesem"
            return render(request,"finance/add_opinion.html",{
                "message": message,
                "opinion": opinion
            })
        return render(request, "finance/add_opinion.html")