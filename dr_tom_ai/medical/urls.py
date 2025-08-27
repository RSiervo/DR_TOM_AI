from django.urls import path
from . import views

urlpatterns = [
    path('', views.analyze_view, name='analyze'),
    path('history/', views.history_view, name='history'),
    path("privacy/", views.privacy_view, name="privacy"),
    path('consultation/<int:pk>/', views.consultation_detail, name='consultation_detail'),
    path('consultation/<int:pk>/pdf/', views.consultation_pdf, name='consultation_pdf'),
]

