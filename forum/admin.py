from django.contrib import admin

from .models import ForumThread, Rating, Comment, Topic #ForumUser,

# admin.site.register(ForumUser)
admin.site.register(ForumThread)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Topic)
