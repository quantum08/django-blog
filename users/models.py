from django.db import models
from django.contrib.auth.models import User

#for resize the image
from PIL import Image
# Create your models here.

class Profile(models.Model):


    #for one to one relation between User and its profile
    user = models.OneToOneField(User , on_delete=models.CASCADE)

    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username


# To Resize the Image

    def save(self, *args ,**kwargs):
        super().save(*args , **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
