from django.urls import path
from .api import user_register, user_login, user_logout, pokemon_list, pokemon_detail, retrieve_random_number

urlpatterns = [
    path('register/', user_register, name = 'api_user_registration'),
    path('login/', user_login, name = 'api_user_login'),
    path('logout/', user_logout, name = 'api_user_logout'),
    path('pokemons/', pokemon_list, name = 'api_pokemon_fetch'),
    path('pokemons/<int:pokemon_id>/', pokemon_detail, name = 'api_pokemon_detail'),
    path('random/', retrieve_random_number, name = 'retrieve_random_number'),
]
