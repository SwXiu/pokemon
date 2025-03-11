# views.py
from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpResponse
from .models import Pokemon

def insertarPokemon(request):
    url = "https://pokeapi.co/api/v2/pokemon?limit=503"
    response = requests.get(url)
    if response.status_code != 200:
        return HttpResponse("Error al obtener los datos de la API", status=500)
    
    all_pokemon = response.json()["results"]
    for pokemon in all_pokemon:
        pokemon_data = requests.get(pokemon["url"]).json()
        types = [t["type"]["name"] for t in pokemon_data["types"]]
        image = pokemon_data["sprites"]["front_default"]
        Pokemon.objects.create(name=pokemon["name"], types=",".join(types), image=image)
    
    return HttpResponse("Datos insertados correctamente", status=200)

def getPokemonData(request, pokemon_id): 
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        formatted_id = f"{data['id']:03d}"

        pokemon_info = {
            "name": data["name"],
            "id": formatted_id,
            "sprite": data["sprites"]["front_default"],
            "types": [t["type"]["name"] for t in data["types"]],
        }
        
        return render(request, 'index.html', {'pokemon': pokemon_info})
        
    except requests.exceptions.HTTPError as e:
        return HttpResponse(f"Error: Pokémon con ID {pokemon_id} no encontrado", status=404)
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error de conexión: {str(e)}", status=500)

def getPokemonList(request):
    query = request.GET.get('query', '').lower()
    url = "https://pokeapi.co/api/v2/pokemon?limit=1000"

    response = requests.get(url)
    if response.status_code != 200:
        return JsonResponse({'suggestions': []})

    all_pokemon = response.json()['results']

    suggestions = [
        {"name": p["name"], "id": p["url"].split("/")[-2]}
        for p in all_pokemon if query in p["name"]
    ]
    print(suggestions)
    return JsonResponse({'suggestions': suggestions})