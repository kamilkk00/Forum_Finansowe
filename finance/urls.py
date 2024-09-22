from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login_view"),
    path("register/", views.register, name="register"), 
    path("logout/", views.logout_view, name="logout_view"),
    path("create/", views.create, name="create"),
    path("profile/<str:user_username>", views.profile, name="profile"),
    path("post/<str:post_id>", views.post_page, name="post_page"),
    path("create_professional/", views.create_professional, name="create_professional"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:post_category>", views.category, name="category"),
    path("profile/<str:username>/professional", views.professional_profile, name="professional_profile"),
    path("search/subject", views.search_subject, name="search_subject"),
    path("search/content", views.search_content, name="search_content"),
    path("saved/post/detail/all", views.saved_post_all_detail, name="all_saved_post"),
    path("saved/post/detail/<str:post_id>", views.saved_post_id, name="saved_post"),
    path("detail/save/post/<str:post_id>", views.save_post_detail, name="save_post"),
    path("saved/user/<str:user_username>", views.view_saved_posts, name="view_saved_posts"),
    path("detail/like/post/<str:post_id>", views.detail_like_post, name="detail_like_post"),
    path("save/like/<str:post_id>", views.like_function, name="like_function"),
    path("detail/comment/like/post/<str:comment_id>", views.detail_like_comment, name="detail_like_comment"),
    path("save/comment/like/<str:comment_id>", views.add_like_comment, name="add_like_comment"),
    path("save/edit/post/<str:post_id>", views.edit_post, name="edit_post"),
    path("save/edit/comment/<str:comment_id>", views.edit_comment, name="edit_comment"),
    path("profile/<str:username>/professional/add/opinion", views.add_opinion, name="add_opinion")
]