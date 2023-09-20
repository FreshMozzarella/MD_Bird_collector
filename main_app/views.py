from django.shortcuts import render
from .models import Bird
from .api import fetch_bird_calls_from_xenocanto, fetch_image_from_inaturalist
import requests
from django.views.decorators.cache import cache_page

# Define the home view
def home(request):
 
  return render(request, 'home.html')

def about(request):
  
  return render(request, 'about.html')

@cache_page(60 * 15)
def birds_index(request):
    try:
        # Fetch bird data from Xeno-Canto
        recordings = fetch_bird_calls_from_xenocanto()
    except Exception as e:
        # Log the exception 
        print(f"Error fetching from Xeno-Canto: {e}")
        return render(request, 'error_template.html', {
            'message': 'Failed to fetch data from Xeno-Canto'
        })

    # Set to keep track of species we've seen
    seen_species = set()

    # List to store unique species recordings
    unique_recordings = []

    # iNaturalist token expires in 24 hours
    access_token = "eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjo3NDI3ODcxLCJleHAiOjE2OTUzMTg2Mjh9.LPHWZImGCvO9SExggffDtbhmeo87MxOY2Y2_XaoWeZdT8XdTHk0A87YNtmfHoPegbgYURKeCdd4ar2QPnRlLlA"

    for recording in recordings:
        species_name = recording['gen'] + " " + recording['sp']

        # If the species is unique and hasn't been processed yet
        if species_name not in seen_species:
            try:
                recording['image_url'] = fetch_image_from_inaturalist(species_name, access_token)
                unique_recordings.append(recording)
                seen_species.add(species_name)
            except Exception as e:
                # Log the exception!
                print(f"Error fetching image from iNaturalist for {species_name}: {e}")
                recording['image_url'] = None  # Default to no image if there's an error
        
        # Stop once we've processed 10 unique species
        if len(unique_recordings) >= 10:
            break

    return render(request, 'birds/index.html', {
        'recordings': unique_recordings
    })


