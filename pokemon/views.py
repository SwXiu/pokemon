# views.py
from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpResponse

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
    url = "https://pokeapi.co/api/v2/pokemon?limit=101"

    response = requests.get(url)
    if response.status_code != 200:
        return JsonResponse({'suggestions': []})

    all_pokemon = response.json()['results']
    suggestions = [
        {"name": p["name"], "id": p["url"].split("/")[-2]}
        for p in all_pokemon if query in p["name"]
    ]
    
    return JsonResponse({'suggestions': suggestions})