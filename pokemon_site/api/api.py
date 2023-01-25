from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer, PokemonSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from .models import User, Pokemon
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import requests
from .pagination import CustomPagination

# REGISTER, LOGIN AND LOGOUT
@api_view(['POST'])
def user_register(req):
    if req.method == 'POST':
        serializer = UserRegistrationSerializer(data = req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(req):
    if req.method == 'POST':
        serializer = UserLoginSerializer(data = req.data)
        if serializer.is_valid():
            email = req.data['email']
            if not len(User.objects.filter(email = email)):
                msg = {'msg': 'El email ingresado no está registrado, ingresa con un email registrado para poder ingresar'}
                return Response(msg, status = status.HTTP_400_BAD_REQUEST)
            password = req.data['password']
            user_profile = authenticate(email = email, password = password)
            if user_profile is not None:
                token, _ = Token.objects.get_or_create(user = user_profile)
                if token:
                    login(req, user_profile)
                    return Response({'msg': 'Autenticado exitosamente'}, status = status.HTTP_200_OK)
            else:
                return Response({'msg': 'Contraseña incorrecta, intenta de nuevo'}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'Email no valido, ingrese un email válido'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_logout(req):
    if req.method == 'POST':
        if req.user.is_authenticated:
            # req.user.auth_token.delete()
            logout(req)
            return Response({'msg': 'Desconectado exitosamente'}, status = status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'No estas logueado'}, status = status.HTTP_400_BAD_REQUEST)

# POKEMON API
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def pokemon_list(req):
    if req.method == 'GET': # Fetch all pokemons that user have
        pagination_class = CustomPagination
        paginator = pagination_class()
        user = User.objects.get(email = req.user.email)
        pokemons = Pokemon.objects.filter(user = user.id)
        public_pokemons = Pokemon.objects.filter(public = True).exclude(user = req.user)
        all_pokemons = list(pokemons) + list(public_pokemons)
        page = paginator.paginate_queryset(all_pokemons, req)
        serializer = PokemonSerializer(page, many = True)
        return paginator.get_paginated_response(serializer.data)

    elif req.method == 'POST': # Create a new pokemon that user have
        serializer = PokemonSerializer(data = req.data)
        if serializer.is_valid():
            if req.user.email != req.data['user']:
                return Response({'msg': 'Debes ingresar tu email'}, status = status.HTTP_400_BAD_REQUEST)
            race = req.data['race']
            category = req.data['category']
            health = req.data['health']
            defense = req.data['defense']
            special_attack = req.data['special_attack']
            pokemon = Pokemon(user = req.user, race = race, category = category, health = health, defense = defense, special_attack = special_attack)
            pokemon.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def pokemon_detail(req, pokemon_id):
    if req.method == 'GET': # Get one pokemon BY it's ID
        query = Pokemon.objects.filter(id = pokemon_id)
        if len(query):
            user_query = query.filter(user = req.user)
            public_query = query.filter(public = True)
        else:
            return Response({'msg': f'Pokemon no encontrado con id {pokemon_id}'}, status = status.HTTP_404_NOT_FOUND)
        pokemon = None
        if len(user_query) or len(public_query):
            pokemon = user_query[0] if len(user_query) else public_query[0]
            serializer = PokemonSerializer(pokemon)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({'msg': f'El pokemon con id {pokemon_id} no es tuyo!. No puedes traerlo!'}, status = status.HTTP_404_NOT_FOUND)

    pokemon = Pokemon.objects.filter(id = pokemon_id)
    if not len(pokemon):
        return Response({'msg': f'No existe pokemon con id {pokemon_id}'}, status = status.HTTP_404_NOT_FOUND)
    
    try:
        pokemon = pokemon.get(user = req.user)
    except Pokemon.DoesNotExist:
        return Response({'msg': f'El pokemon con id {pokemon_id} no es tuyo!. No puedes eliminarlo ni actualizarlo!'}, status = status.HTTP_403_FORBIDDEN)

    if req.method == 'PUT': # Update a pokemon by it's ID
        serializer = PokemonSerializer(pokemon, data = req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif req.method == 'DELETE': # Delete a pokemon by it's ID
        pokemon.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def retrieve_random_number(req): # RETRIEVE A RANDOM NUMBER
    if req.method == 'GET':
        query = {'min': 0, 'max': 10**8, 'count': 1}
        ans = requests.get('http://www.randomnumberapi.com/api/v1.0/random', params = query).json()[0]
        return Response({'random number': ans})
