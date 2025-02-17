from django.contrib import admin
from django.urls import path
from . import views

app_name = 'pokemon'

urlpatterns = [
    path('<int:pokemon_id>/', views.getPokemonData, name='getData'),
    path('pokemonList/', views.getPokemonList, name='getList'),
]
