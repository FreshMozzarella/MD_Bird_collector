from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import BirdDetailView, BirdUpdateView, BirdDeleteView

urlpatterns = [
path('', views.home, name='home'),
path('about/', views.about, name='about'),
path('birds/', views.birds_index, name='birds_index'),
path('create_bird/', views.create_bird, name='create_bird'),
path('birds/<int:pk>/', BirdDetailView.as_view(), name='bird_detail'),
path('birds/<int:pk>/edit/', BirdUpdateView.as_view(), name='bird_edit'),
path('birds/<int:pk>/delete/', BirdDeleteView.as_view(), name='bird_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)