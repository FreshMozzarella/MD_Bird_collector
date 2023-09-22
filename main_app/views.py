from django.shortcuts import render
from .models import Bird
from .api import fetch_bird_calls_from_xenocanto, fetch_image_from_inaturalist
import requests
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect
from .forms import BirdForm
from django.core.files import File
from urllib.request import urlopen
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
    # iNaturalist token expires in 24 hours
access_token = 'eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjo3NDI3ODcxLCJleHAiOjE2OTU0MTQ1NTh9.rA002RP4olpmnizLJdSeYmDJ-qVH57PLwVv3PF5sJ8N3DePgYNkI2qboaStY3NvmbJFOSenSUC14KNIcLmh3zA'

# Define the home view
def home(request):
 
  return render(request, 'home.html')

def about(request):
  
  return render(request, 'about.html')

# @cache_page(60 * 15)
def birds_index(request):
    # Retrieve the first 10 birds from the database (you can adjust this as per your needs)
    birds = Bird.objects.all()

    return render(request, 'birds/index.html', {
        'birds': birds
    })

def store_birds_in_database(access_token):  
    try:
        recordings = fetch_bird_calls_from_xenocanto()
    except Exception as e:
        print(f"Error fetching from Xeno-Canto: {e}")
        return

    seen_species = set()
    count_saved = 0

    for recording in recordings:
        species_name = recording['gen'] + " " + recording['sp']
        
        if species_name in seen_species:
            continue

        seen_species.add(species_name)

        # Check if this recording (based on catalogue number) already exists in the database
        exists = Bird.objects.filter(catalogue_number=recording['id']).exists()
        
        if not exists and recording['lat'] and recording['lng']:
            try:
                bird = Bird.objects.create(
                    catalogue_number=recording['id'],
                    gen=recording['gen'],
                    sp=recording['sp'],
                    ssp=recording['ssp'],
                    group=recording['group'],
                    en=recording['en'],
                    rec=recording['rec'],
                    cnt=recording['cnt'],
                    loc=recording['loc'],
                    lat=float(recording['lat']) if recording['lat'] is not None else None,
                    lng=float(recording['lng']) if recording['lng'] is not None else None,
                    sound_type=recording['type'],
                    sex=recording['sex'],
                    stage=recording['stage'],
                )

                image_url = fetch_image_from_inaturalist(species_name, access_token)
                if image_url:
                    save_file_from_url(bird.image, image_url)

                audio_url = recording['file']
                if audio_url:
                    save_file_from_url(bird.audio, audio_url)

                count_saved += 1
            except Exception as e:
                print(f"Error saving {species_name}: {e}")

            # Stop once we've processed 10 unique species
            if count_saved >= 10:
                break

def create_bird(request):
    if request.method == 'POST':
        form = BirdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bird saved successfully!')  # Add a success message
            return redirect('birds_index')
        else:
            messages.error(request, 'There was an error saving the bird.')  # Add an error message
            for field, error in form.errors.items():  # Loop through the form errors
                messages.error(request, f"{field}: {error}")  # Add each error as a message
    else:
        form = BirdForm()

    context = {'form': form}
    return render(request, 'main_app/create_bird.html', context)

def save_file_from_url(model_field, url):
    temp_file = urlopen(url)
    model_field.save(
        f"{url.split('/')[-1]}",  # Extract filename from URL to use as the name
        File(temp_file),
        save=True
    )

# def bird_detail(request, bird_id):
#     bird = get_object_or_404(Bird, id=bird_id)
#     return render(request, 'main_app/bird_detail.html', {'bird': bird})

class BirdDetailView(DetailView):
    model = Bird
    template_name = "main_app/bird_detail.html"

class BirdUpdateView(UpdateView):
    model = Bird
    template_name = "main_app/create_bird.html"
    form_class = BirdForm
    exclude = ['catalogue_number']

    def get_success_url(self):
        return reverse_lazy('bird_detail', kwargs={'pk': self.object.pk})
    
class BirdDeleteView(DeleteView):
    model = Bird
    template_name = "main_app/bird_confirm_delete.html"
    success_url = reverse_lazy('birds_index')