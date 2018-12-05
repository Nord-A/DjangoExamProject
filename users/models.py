from django.db import models
from django.contrib.auth.models import User
from PIL import Image

#class User(models.Model):
    #name = models.CharField(max_length=30)
    #username = models.CharField(max_length=20)
    #password = models.CharField(max_length=20)
    # email = models.CharField(max_length=30)
    #email = models.EmailField()
    #datetime_created = models.DateTimeField(default=timezone.now)
    #is_active = models.BooleanField(default=True)

        #image = models.ImageField()

    #def __str__(self):
        #return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

