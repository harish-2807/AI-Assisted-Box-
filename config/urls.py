from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('box_selection.urls')),
    path('', lambda request: redirect('product-list-create', permanent=False)),
]
