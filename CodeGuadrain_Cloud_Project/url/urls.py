from django.urls import path
from .views import index, generate_report
from django.conf import settings
from django.conf.urls.static import static

app_name = 'url'

urlpatterns = [
    path('', index, name='index'),
    path('submit/analyze/', generate_report, name='generate_report'),  # Changed URL pattern
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)