from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from medical.views import home_view

urlpatterns = [
    path('', home_view, name='home'),           # landing page
    path('app/', include('medical.urls')),      # the app
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
