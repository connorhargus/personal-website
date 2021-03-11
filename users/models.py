from django.db import models
from django.contrib.auth.models import User
# from PIL import Image, ImageOps


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}\'s Profile'

    # # Override save method to crop/shrink photos for efficiency
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #
    #         # Crop to a square image without stretching image
    #         thumb = ImageOps.fit(img, output_size, Image.ANTIALIAS)
    #         thumb.save(self.image.path)