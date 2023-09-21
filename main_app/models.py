from django.db import models

class Bird(models.Model):
    catalogue_number = models.CharField(max_length=100, unique=True, null=True)
    gen = models.CharField(max_length=100, null=True)
    sp = models.CharField(max_length=100, null=True)
    ssp = models.CharField(max_length=100, blank=True, null=True)  # Subspecies might be optional
    group = models.CharField(max_length=50, null=True)
    en = models.CharField(max_length=200, null=True)
    rec = models.CharField(max_length=200, null=True)
    cnt = models.CharField(max_length=100, null=True)
    loc = models.CharField(max_length=200, null=True)
    lat = models.FloatField(null=False)
    lng = models.FloatField(null=False)
    sound_type = models.CharField(max_length=50, null=True)
    sex = models.CharField(max_length=20, blank=True, null=True) # Sex might be optional
    stage = models.CharField(max_length=50, blank=True, null=True) # Life stage might be optional
    image = models.ImageField(upload_to='bird_images/', null=True)
    audio = models.FileField(upload_to='bird_audio/', null=True)
    def __str__(self):
        return self.en
