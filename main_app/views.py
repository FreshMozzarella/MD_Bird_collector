from django.shortcuts import render
from .models import Bird
from .api import fetch_bird_calls_from_xenocanto, fetch_image_from_inaturalist
import requests
from django.views.decorators.cache import cache_page
# Create your views here.

# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def about(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'about.html')

def is_within_maryland(recording):
    """Check if a recording's latitude and longitude is within Maryland's bounding box."""
    return 37.8 <= float(recording['lat']) <= 39.8 and -79.5 <= float(recording['lon']) <= -75.0
@cache_page(60 * 15)
def birds_index(request):
    try:
        # Fetch bird data from Xeno-Canto
        recordings = fetch_bird_calls_from_xenocanto()
       
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error fetching from Xeno-Canto: {e}")
        return render(request, 'error_template.html', {
            'message': 'Failed to fetch data from Xeno-Canto'
        })
    limited_recordings = recordings[:10]
    # Assuming you have some way to get the iNaturalist access token:
    access_token = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjo3NDI3ODcxLCJleHAiOjE2OTUzMTg2Mjh9.LPHWZImGCvO9SExggffDtbhmeo87MxOY2Y2_XaoWeZdT8XdTHk0A87YNtmfHoPegbgYURKeCdd4ar2QPnRlLlA"

    for recording in limited_recordings:
        try:
            species_name = recording['gen'] + " " + recording['sp']
            recording['image_url'] = fetch_image_from_inaturalist(species_name, access_token)
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error fetching image from iNaturalist for {species_name}: {e}")
            recording['image_url'] = None  # Default to no image if there's an error
    return render(request, 'birds/index.html', {
        'recordings': limited_recordings
    })


