from django.db import models
from django.utils import timezone
from users.models import User


# class ForumUser(models.Model):
#     name = models.CharField(max_length=30)
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     email = models.EmailField()
#     datetime_created = models.DateTimeField(default=timezone.now, editable=False)
#     is_active = models.BooleanField(default=True)
#     # image = models.ImageField()
      #likes
#
#     def __str__(self):
#         return self.username


class Topic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ForumThread(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # owner = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField(max_length=2000) #Limit?
    datetime_created = models.DateTimeField(default=timezone.now, editable=False)
    datetime_edited = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    #Likes/dislikes?

    def __str__(self):
        return self.title
    # Overload save method. copy pasted
    # def save(self, *args, **kwargs):
    #     # if not self.id:
    #     #     self.datetime_created = timezone
    #     self.datetime_edited = timezone.now()
    #     return super(ForumThread, self).save(*args, **kwargs)


class Comment(models.Model):
    content = models.TextField(max_length=2000) #Limit?
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, null=True)
    datetime_created = models.DateTimeField(default=timezone.now, editable=False)
    datetime_edited = models.DateTimeField(default=timezone.now)
    #Can a comment be commented on?
    # File upload PDF, other

    def __str__(self):
        return self.content


class Rating(models.Model):
    thumps_up = models.BooleanField()
    # user = models.ForeignKey(ForumUser, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.thumps_up
