from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('', views.home, name='home'),
path('about/', views.about, name='about'),
path('birds/', views.birds_index, name='birds_index'),
path('create_bird/', views.create_bird, name='create_bird'),
path('birds/<int:bird_id>/', views.bird_detail, name='bird_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)