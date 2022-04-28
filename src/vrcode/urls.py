from django.urls import path
from . import views


urlpatterns = [
    path('generate-vcf-qr/', views.generate_VCFQR, name='vcf_qr_create'),
]