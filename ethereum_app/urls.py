from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('balance/')),
    path('balance/', include('balance.urls')),
    path('admin/', admin.site.urls),
]
