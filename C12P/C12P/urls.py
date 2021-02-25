from django.contrib import admin
from django.urls import include, path



urlpatterns = [
    path('GoCabs/', include('GoCabs.urls')),
    path('admin/', admin.site.urls)
]
