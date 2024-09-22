from django.contrib import admin
from .models import User, Post, Comment, ProfessionalUser, Like, Like_Comment, Save_Post, Rating_User

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ProfessionalUser)
admin.site.register(Like)
admin.site.register(Like_Comment)
admin.site.register(Save_Post)
admin.site.register(Rating_User)