'''
Created on Jan 30, 2025

@author: Giuseppe
'''
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    ]
