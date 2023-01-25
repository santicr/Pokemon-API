# Pokemon-API
A Pokemon API with authorization and authentication

# How to run?
# Prerequisites
## Python installation
Follow this link and look for your operative system (MAC OS / LINUX / WINDOWS) and follow steps: <br> https://www.tutorialsteacher.com/python/install-python

## Pip installation
Follow this link if you are a Windows 10/11 user and follow steps: <br>
https://www.geeksforgeeks.org/how-to-install-pip-on-windows/

Follow this link if you are a Linux user and follow steps: <br>
https://parzibyte.me/blog/2019/06/07/instalar-pip-3-linux-ubuntu/

Follow this link if you are a MAC OS user and follow steps: <br>
[Pip installation for MAC](https://www.groovypost.com/howto/install-pip-on-a-mac/#:~:text=To%20install%20PIP%20using%20ensurepip,instructions%20to%20complete%20this%20process)

## Github installation, cloning the project, downloading project requirements and running the project
For Github Desktop installation (MAC and WINDOWS) follow this link: <br>
https://desktop.github.com/ <br>
For cloning my project: <br>
1. Sign in to GitHub.com and GitHub Desktop before you start to clone.
2. Copy this link: https://github.com/santicr/Pokemon-API
3. Go to this [link](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop) and **follow the tutorial from step #3**
4. Once you finished, locate the folder with the project "Pokemon-API"
5. Open CMD / Terminal and go to the "Pokemon-API" folder location
6. Once you're there, just type <br> ``pip3 install -r requirements.txt`` <br> or <br> ``pip install -r requirements``
7. Now, go to "pokemon_site" folder location using CMD / TERMINAL, then type: <br>
``python manage.py runserver`` <br> or <br> ``python3.10 manage.py runserver``
8. Done!

## Api endpoints
These all are urls that works: <br>
This endpoint is for register a new user: http://127.0.0.1:8000/api/1.0/register/ <br>
This endpoint is for login with registered user: http://127.0.0.1:8000/api/1.0/login/ <br>
This endpoint is for logout when user is logged: http://127.0.0.1:8000/api/1.0/logout/ <br>
This endpoint is for fetch all user pokemons: http://127.0.0.1:8000/api/1.0/pokemons/ <br>
This endpoint is for fetch an user pokemon by it's id: http://127.0.0.1:8000/api/1.0/pokemons/1/ <br>
This endpoint is for retrieve a random number from an existing API: http://127.0.0.1:8000/api/1.0/random/ <br>

**IMPORTANT**
For user post requests copy the followint as a body:

{
  "email": "mail@gmail.com",
  "password": "Mail12345@"
}

For pokemon post/put requests copy the following as a body:

{
  "race": "RareMixedWaterNFire",
  "category": "Water and Fire",
  "health": 50,
  "defense": 50,
  "special_attack": "Fire ball and water ball",
  "user": "mail@gmail.com",
  "public": true
}
