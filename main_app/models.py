from django.db import models
class Bird(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image_url = models.URLField()
    audio_url = models.URLField()

    def __str__(self):
        return self.name
# Create your models here.
