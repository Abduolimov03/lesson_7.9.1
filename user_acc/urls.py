from django.urls import path
from .views import *

urlpatterns = [
    path('regis/', RegisterApi.as_view())
]