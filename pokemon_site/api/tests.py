from django.test import TestCase
from api.models import User, Pokemon
import requests, re
from requests.auth import HTTPBasicAuth

# Create your tests here.
class LoginTestCase1(TestCase):
    def setUp(self) -> None:
        self.email = "falseemail@gmail.com"
        self.users_len = len(User.objects.filter(email = self.email))
        pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        pattern_match = True if re.match(pattern, self.email) else False
        self.assertEqual(self.users_len, 0)
        self.assertEqual(pattern_match, True)

    def test_login_email_not_registered(self):
        data = {'email': self.email, 'password': 'Whatever1234@'}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/login/', data = data).json()['msg']
        expected_ans = 'El email ingresado no está registrado, ingresa con un email registrado para poder ingresar'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        self.users_len = len(User.objects.filter(email = self.email))
        self.assertEqual(self.users_len, 0)

class LoginTestCase2(TestCase):
    def setUp(self) -> None:
        self.email = "fakeemail@adios"
        pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        pattern_match = True if re.match(pattern, self.email) else False
        self.assertEqual(pattern_match, False)

    def test_login_invalid_email(self):
        data = {'email': self.email, 'password': 'Whatever1234@'}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/login/', data = data).json()['msg']
        expected_ans = 'Email no valido, ingrese un email válido'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        pattern_match = True if re.match(pattern, self.email) else False
        self.assertEqual(pattern_match, False)

class LoginTest3(TestCase):
    def setUp(self) -> None:
        pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        self.email = 'mail@gmail.com'
        self.password = 'Whatever1234@'
        pattern_match = True if re.match(pattern, self.email) else False
        self.users_len = len(User.objects.filter(email = self.email))
        self.assertEqual(pattern_match, True)

    def test_login_correct_email_wrong_password(self):
        data = {'email': self.email, 'password': self.password}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/login/', data = data).json()['msg']
        expected_ans = 'Contraseña incorrecta, intenta de nuevo'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        self.email = 'mail@gmail.com'
        self.password = 'Whatever1234@'

class LoginTest4(TestCase):
    def setUp(self) -> None:
        self.pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        self.email = 'mail@gmail.com'
        self.password = 'Mail12345@'
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.users_len = len(User.objects.filter(email = self.email))
        self.assertEqual(pattern_match, True)

    def test_login_correct_email_and_password(self):
        data = {'email': self.email, 'password': self.password}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/login/', data = data).json()['msg']
        expected_ans = 'Autenticado exitosamente'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.users_len = len(User.objects.filter(email = self.email))
        self.assertEqual(pattern_match, True)

class RegisterTest1(TestCase):
    def setUp(self) -> None:
        self.pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        self.email = 'mail@gmail.'
        self.password = 'Whatever12345@'
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, False)

    def test_register_invalid_email(self):
        data = {'email': self.email, 'password': self.password}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/register/', data = data).json()['email']
        expected_ans = ['Introduzca una dirección de correo electrónico válida.']
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, False)

class RegisterTest2(TestCase):
    def setUp(self) -> None:
        self.pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        self.email = 'gmail@gmail.com'
        self.password = 'Whatever@'
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)
        self.assertLess(len(self.password), 10)

    def test_register_short_password(self):
        data = {'email': self.email, 'password': self.password}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/register/', data = data).json()['password']
        expected_ans = ['La contraseña está muy corta, debe ser de al menos 10 dígitos']
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)

class RegisterTest3(TestCase):
    def setUp(self) -> None:
        self.pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        self.email = 'gmail@gmail.com'
        self.password = 'whateveragain@'
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)
        self.assertGreaterEqual(len(self.password), 10)

    def test_register_no_capital_letters(self):
        data = {'email': self.email, 'password': self.password}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/register/', data = data).json()['password']
        expected_ans = ['La contraseña debe contener una letra en mayúscula']
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)
        self.assertGreaterEqual(len(self.password), 10)

class RegisterTest4(TestCase):
    def setUp(self) -> None:
        self.pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        self.email = 'gmail@gmail.com'
        self.password = 'WHATEVERAGAIN@'
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)
        self.assertGreaterEqual(len(self.password), 10)

    def test_register_no_lowercase(self):
        data = {'email': self.email, 'password': self.password}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/register/', data = data).json()['password']
        expected_ans = ['La contraseña debe contener una letra en minúscula']
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)
        self.assertGreaterEqual(len(self.password), 10)

class RegisterTest5(TestCase):
    def setUp(self) -> None:
        self.pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        self.email = 'gmail@gmail.com'
        self.password = 'Whatever12345'
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)
        self.assertGreaterEqual(len(self.password), 10)

    def test_register_no_special_chars(self):
        data = {'email': self.email, 'password': self.password}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/register/', data = data).json()['password']
        expected_ans = ['La contraseña debe contener al menos uno de estos caracteres: @, !, #, ? o ]']
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)
        self.assertGreaterEqual(len(self.password), 10)

class RegisterTest6(TestCase):
    def setUp(self) -> None:
        self.pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        self.email = 'mail@gmail.com'
        self.password = 'Whatever12345@'
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)
        self.assertGreaterEqual(len(self.password), 10)

    def test_register_registered_email(self):
        data = {'email': self.email, 'password': self.password}
        ans = requests.post('http://127.0.0.1:8000/api/1.0/register/', data = data).json()['email']
        expected_ans = ['Este email ya está registrado, ingrese uno nuevo']
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pattern_match = True if re.match(self.pattern, self.email) else False
        self.assertEqual(pattern_match, True)
        self.assertGreaterEqual(len(self.password), 10)

# class RegisterTest6(TestCase):
#     def setUp(self) -> None:
#         self.pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
#         self.email = 'newsstestmail@gmail.com'
#         self.password = 'Whatever12345@'
#         pattern_match = True if re.match(self.pattern, self.email) else False
#         self.assertEqual(pattern_match, True)
#         self.assertGreaterEqual(len(self.password), 10)

#     def test_register_not_registered_email_and_correct_password(self):
#         data = {'email': self.email, 'password': self.password}
#         ans = requests.post('http://127.0.0.1:8000/api/1.0/register/', data = data).json()['email']
#         expected_ans = self.email
#         self.assertEqual(ans, expected_ans)

#     def tearDown(self) -> None:
#         pattern_match = True if re.match(self.pattern, self.email) else False
#         self.assertEqual(pattern_match, True)
#         self.assertGreaterEqual(len(self.password), 10)

class PokemonApiGetTest1(TestCase):
    def setUp(self) -> None:
        # User.objects.create(email = "new_fake_email@gmail.com", password = "Hello12345@")
        # Pokemon(user = self.user, race = "Pikachu", category = "Thunder", health = 1, defense = 23, special_attack = "Thunder ball")
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'
        self.pokemon_id = 90

    def test_fetch_pokemon_not_created(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        ans = requests.get(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
            auth = HTTPBasicAuth(username = self.email, password = self.password)
        ).json()['msg']
        expected_ans = f'Pokemon no encontrado con id {self.pokemon_id}'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass


class PokemonApiGetTest2(TestCase):
    def setUp(self) -> None:
        # User.objects.create(email = "new_fake_email@gmail.com", password = "Hello12345@")
        # Pokemon(user = self.user, race = "Pikachu", category = "Thunder", health = 1, defense = 23, special_attack = "Thunder ball")
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'
        self.pokemon_id = 5

    def test_fetch_pokemon_not_own(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        ans = requests.get(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
            auth = HTTPBasicAuth(username = self.email, password = self.password)
        ).json()['msg']
        expected_ans = f'El pokemon con id {self.pokemon_id} no es tuyo!. No puedes traerlo!'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiGetTest3(TestCase):
    def setUp(self) -> None:
        # Already created a pokemon to user newtestmail@gmail.com
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'
        self.pokemon_id = 7

    def test_fetch_pokemon_own(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        ans = requests.get(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
            auth = HTTPBasicAuth(username = self.email, password = self.password)
        ).status_code
        expected_ans = 200
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiGetTest4(TestCase):
    def setUp(self) -> None:
        # Already created a pokemon to user newtestmail@gmail.com
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'
        self.pokemon_id = 7

    def test_fetch_all_pokemon(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        ans = requests.get(
            f'http://127.0.0.1:8000/api/1.0/pokemons/',
            auth = HTTPBasicAuth(username = self.email, password = self.password)
        ).status_code
        expected_ans = 200
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiGetTest5(TestCase):
    def setUp(self) -> None:
        # Already created a pokemon to user newtestmail@gmail.com
        self.pokemon_id = 7

    def test_fetch_no_auth(self):
        ans = requests.get(
            f'http://127.0.0.1:8000/api/1.0/pokemons/',
        ).json()['detail']
        expected_ans = 'Las credenciales de autenticación no se proveyeron.'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiPostTest1(TestCase):
    def setUp(self) -> None:
        # Already created a pokemon to user newtestmail@gmail.com
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'
        self.pokemon_id = 7

    def test_post_wrong_email(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        data = {
            "race": "Pikachu",
            "category": "Water and Fire",
            "health": 1,
            "defense": 1,
            "special_attack": "Fire ball and water ball",
            "user": "mail@gmail.com",
            "public": False
        }
        ans = requests.post(
            f'http://127.0.0.1:8000/api/1.0/pokemons/',
            auth = HTTPBasicAuth(username = self.email, password = self.password),
            data = data
        ).json()['msg']
        expected_ans = 'Debes ingresar tu email'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiPostTest2(TestCase):
    def setUp(self) -> None:
        # Already created a pokemon to user newtestmail@gmail.com
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'
        self.pokemon_id = 7

    def test_post_correct_data(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        data = {
            "race": "Pikachu",
            "category": "Water and Fire",
            "health": 1,
            "defense": 1,
            "special_attack": "Fire ball and water ball",
            "user": "newtestmail@gmail.com",
            "public": False
        }
        ans = requests.post(
            f'http://127.0.0.1:8000/api/1.0/pokemons/',
            auth = HTTPBasicAuth(username = self.email, password = self.password),
            data = data
        ).status_code
        expected_ans = 201
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiPostTest3(TestCase):
    def setUp(self) -> None:
        # Already created a pokemon to user newtestmail@gmail.com
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'
        self.pokemon_id = 7

    def test_post_wrong_data(self):
        data = {
            'email': self.email,
            'password': self.password
        }
        data = {
            "category": "Water and Fire",
            "health": 1,
            "defense": 1,
            "special_attack": "Fire ball and water ball",
            "user": "newtestmail@gmail.com",
            "public": False
        }
        ans = requests.post(
            f'http://127.0.0.1:8000/api/1.0/pokemons/',
            auth = HTTPBasicAuth(username = self.email, password = self.password),
            data = data
        ).status_code
        expected_ans = 400
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiPostTest4(TestCase):
    def setUp(self) -> None:
        # Already created a pokemon to user newtestmail@gmail.com
        pass

    def test_post_no_auth(self):
        data = {
            "category": "Water and Fire",
            "health": 1,
            "defense": 1,
            "special_attack": "Fire ball and water ball",
            "user": "newtestmail@gmail.com",
            "public": False
        }
        ans = requests.post(
            f'http://127.0.0.1:8000/api/1.0/pokemons/',
            data = data
        ).json()['detail']
        expected_ans = 'Las credenciales de autenticación no se proveyeron.'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiPutTest1(TestCase):
    def setUp(self) -> None:
        self.pokemon_id = 92323
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'

    def test_put_pokemon_doesnt_exist(self):
        data = {
            "race": "Pikachus",
            "category": "Water and Fire",
            "health": 1,
            "defense": 1,
            "special_attack": "Fire ball and water ball",
            "user": "newtestmail@gmail.com",
            "public": False
        }
        
        ans = requests.put(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
            auth = HTTPBasicAuth(username = self.email, password = self.password),
            data = data
        ).json()['msg']
        expected_ans = f'No existe pokemon con id {self.pokemon_id}'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiPutTest2(TestCase):
    def setUp(self) -> None:
        self.pokemon_id = 5
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'

    def test_put_pokemon_not_own(self):
        data = {
            "race": "Pikachus",
            "category": "Water and Fire",
            "health": 1,
            "defense": 1,
            "special_attack": "Fire ball and water ball",
            "user": "newtestmail@gmail.com",
            "public": False
        }
        ans = requests.put(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
            auth = HTTPBasicAuth(username = self.email, password = self.password),
            data = data
        ).json()['msg']
        expected_ans = f'El pokemon con id {self.pokemon_id} no es tuyo!. No puedes eliminarlo ni actualizarlo!'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiPutTest3(TestCase):
    def setUp(self) -> None:
        self.pokemon_id = 10
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'

    def test_put_pokemon_own(self):
        data = {
            "race": "Pikachus",
            "category": "Water and Fire",
            "health": 1,
            "defense": 1,
            "special_attack": "Fire ball and water ball",
            "user": "newtestmail@gmail.com",
            "public": False
        }
        ans = requests.put(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
            auth = HTTPBasicAuth(username = self.email, password = self.password),
            data = data
        ).status_code
        expected_ans = 200
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiPutTest4(TestCase):
    def setUp(self) -> None:
        self.pokemon_id = 10
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'

    def test_put_bad_request(self):
        data = {
            "category": "Water and Fire",
            "health": 1,
            "defense": 1,
            "special_attack": "Fire ball and water ball",
            "user": "newtestmail@gmail.com",
            "public": False
        }
        ans = requests.put(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
            auth = HTTPBasicAuth(username = self.email, password = self.password),
            data = data
        ).status_code
        expected_ans = 400
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiPutTest5(TestCase):
    def setUp(self) -> None:
        self.pokemon_id = 10

    def test_put_no_auth(self):
        data = {
            "category": "Water and Fire",
            "health": 1,
            "defense": 1,
            "special_attack": "Fire ball and water ball",
            "user": "newtestmail@gmail.com",
            "public": False
        }
        ans = requests.put(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
        ).status_code
        expected_ans = 403
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiDeleteTest1(TestCase):
    def setUp(self) -> None:
        self.pokemon_id = 92323
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'

    def test_delete_pokemon_doesnt_exist(self):
        ans = requests.delete(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
            auth = HTTPBasicAuth(username = self.email, password = self.password),
        ).json()['msg']
        expected_ans = f'No existe pokemon con id {self.pokemon_id}'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

class PokemonApiDeleteTest2(TestCase):
    def setUp(self) -> None:
        self.pokemon_id = 5
        self.email = "newtestmail@gmail.com"
        self.password = 'Whatever12345@'

    def test_delete_pokemon_not_own(self):
        ans = requests.delete(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
            auth = HTTPBasicAuth(username = self.email, password = self.password),
        ).json()['msg']
        expected_ans = f'El pokemon con id {self.pokemon_id} no es tuyo!. No puedes eliminarlo ni actualizarlo!'
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass

# class PokemonApiDeleteTest3(TestCase):
#     def setUp(self) -> None:
#         self.pokemon_id = 11
#         self.email = "newtestmail@gmail.com"
#         self.password = 'Whatever12345@'

#     def test_delete_pokemon_own(self):
#         ans = requests.delete(
#             f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
#             auth = HTTPBasicAuth(username = self.email, password = self.password),
#         ).status_code
#         expected_ans = 204
#         self.assertEqual(ans, expected_ans)

#     def tearDown(self) -> None:
#         pass

class PokemonApiDeleteTest4(TestCase):
    def setUp(self) -> None:
        self.pokemon_id = 10

    def test_put_no_auth(self):
        ans = requests.delete(
            f'http://127.0.0.1:8000/api/1.0/pokemons/{self.pokemon_id}/',
        ).status_code
        expected_ans = 403
        self.assertEqual(ans, expected_ans)

    def tearDown(self) -> None:
        pass