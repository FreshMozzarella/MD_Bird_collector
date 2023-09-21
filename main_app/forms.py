from django.core.exceptions import ValidationError
from django import forms
from .models import Bird

def validate_file_extension(value):
    if value.file.content_type != 'audio/wav':
        raise ValidationError(u'Error message')

class BirdForm(forms.ModelForm):
    class Meta:
        model = Bird
        fields = '__all__'
        labels = {
            "catalogue_number": "ID: the catalogue number of the recording on xeno-canto",
            "gen": "Gen: the generic name of the species",
            "sp": "the specific name (epithet) of the species",
            "ssp": "the subspecies name (subspecific epithet)",
            "group": "the group to which the species belongs (birds, grasshoppers, bats)",
            "en": "the English name of the species",
            "rec": "the name of the recordist",
            "cnt": "the country where the recording was made",
            "loc": "the name of the locality",
            "lat": "the latitude of the recording in decimal coordinates",
            "lng": "the longitude of the recording in decimal coordinates",
            "type":"the sound type of the recording (sound, call, chirp)",
            "sex": "the sex of the animal",
            "stage": "the life stage of the animal(adult, juvenile, etc)"
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }