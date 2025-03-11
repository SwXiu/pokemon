document.addEventListener('DOMContentLoaded', function() {
    // URL absoluta para obtener la lista de Pokémon
    var suggestionUrl = "/pokemon/pokemonList/";
    
    // Referencias a los elementos del DOM
    var pokemonInput = document.getElementById('pokemon');
    var suggestionsDiv = document.getElementById('suggestions');

    // Función para obtener y mostrar sugerencias
    function fetchSuggestions(query) {
        $.ajax({
            url: suggestionUrl,
            data: { query: query },
            dataType: "json",
            success: function(response) {
                suggestionsDiv.innerHTML = "";

                if (response.suggestions && response.suggestions.length > 0) {
                    response.suggestions.forEach(function(pokemon) {
                        var item = document.createElement("div");
                        item.className = "suggestion-item";
                        item.style.padding = "8px";
                        item.style.cursor = "pointer";
                        item.style.display = "flex";
                        item.style.alignItems = "center";

                        // Convertir el nombre: primera letra mayúscula, resto minúsculas
                        var displayName = pokemon.name.charAt(0).toUpperCase() + pokemon.name.slice(1).toLowerCase();

                        // Crear imagen del Pokémon usando la URL de los sprites de PokeAPI
                        var img = document.createElement("img");
                        img.src = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/" + pokemon.id + ".png";
                        img.alt = displayName;
                        img.style.width = "30px";
                        img.style.height = "30px";
                        img.style.marginRight = "8px";

                        // Crear un span para el nombre
                        var nameSpan = document.createElement("span");
                        nameSpan.textContent = displayName;
                        nameSpan.style.verticalAlign = "middle";

                        // Agregar la imagen y el nombre al item
                        item.appendChild(img);
                        item.appendChild(nameSpan);

                        // Al hacer clic en la sugerencia, redirige al detalle del Pokémon
                        item.addEventListener("click", function() {
                            window.location.href = "/pokemon/" + pokemon.id + "/";
                        });

                        suggestionsDiv.appendChild(item);
                    });
                    suggestionsDiv.style.display = "block";
                } else {
                    suggestionsDiv.style.display = "none";
                }
            },
            error: function(err) {
                console.error("Error al obtener sugerencias:", err);
            }
        });
    }

    // Al escribir en el input, se buscan sugerencias
    pokemonInput.addEventListener('input', function() {
        var query = pokemonInput.value.trim();
        fetchSuggestions(query);
    });

    // Al hacer clic (o recibir foco) en el input, se muestran las sugerencias (incluso si está vacío)
    pokemonInput.addEventListener('focus', function() {
        var query = pokemonInput.value.trim();
        fetchSuggestions(query);
    });

    // Oculta las sugerencias al hacer clic fuera del input y del div de sugerencias
    document.addEventListener('click', function(e) {
        if (!pokemonInput.contains(e.target) && !suggestionsDiv.contains(e.target)) {
            suggestionsDiv.style.display = "none";
        }
    });

    var insertPokemonUrl = "/pokemon/insertPokemon/";
    $.ajax({
        url: insertPokemonUrl,
        method: "GET",
        success: function(response) {
            console.log("Datos insertados correctamente");
        },
        error: function(err) {
            console.error("Error al insertar datos:", err);
        }
    });
});
