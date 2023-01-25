from rest_framework import serializers
from .models import User

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserRegistrationSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        instance = User()
        instance.email = validated_data.get('email')
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def validate_email(self, data):
        users = User.objects.filter(email = data)
        if len(users):
            raise serializers.ValidationError('Este email ya está registrado, ingrese uno nuevo')
        return data

    def validate_password(self, data):
        special_chars = ['!', '@', '#', '?', ']']
        upper_lower_letters = {'lower': 0, 'upper': 0, 'special_chars': 0}
        if len(data) < 10:
            raise serializers.ValidationError('La contraseña está muy corta, debe ser de al menos 10 dígitos')
        for c in data:
            if c.islower():
                upper_lower_letters['lower'] += 1
            elif c.isupper():
                upper_lower_letters['upper'] += 1
            elif c in special_chars:
                upper_lower_letters['special_chars'] += 1
        
        if not upper_lower_letters['lower']:
            raise serializers.ValidationError('La contraseña debe contener una letra en minúscula')
        if not upper_lower_letters['upper']:
            raise serializers.ValidationError('La contraseña debe contener una letra en mayúscula')
        if not upper_lower_letters['special_chars']:
            raise serializers.ValidationError('La contraseña debe contener al menos uno de estos caracteres: @, !, #, ? o ]')
        
        return data
        
class PokemonSerializer(serializers.Serializer):
    race = serializers.CharField()
    category = serializers.CharField()
    health = serializers.IntegerField()
    defense = serializers.IntegerField()
    special_attack = serializers.CharField()
    user = serializers.CharField(required = False, read_only = True)
    public = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.race = validated_data.get('race', instance.race)
        instance.category = validated_data.get('category', instance.category)
        instance.health = validated_data.get('health', instance.health)
        instance.defense = validated_data.get('defense', instance.defense)
        instance.special_attack = validated_data.get('special_attack', instance.special_attack)
        instance.public = validated_data.get('public', instance.public)
        instance.save()
        return instance