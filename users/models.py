# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default=' ')
    pic = CloudinaryField('pic')#, upload_to='profile_pics'

    def __str__(self):
        return f'{self.user.username} profile'

