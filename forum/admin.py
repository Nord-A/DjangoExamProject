from django.contrib import admin

from .models import ForumUser, ForumThread, Rating, Comment, Topic

admin.site.register(ForumUser)
admin.site.register(ForumThread)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Topic)
