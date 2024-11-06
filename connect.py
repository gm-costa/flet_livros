import requests


URL_API = 'http://127.0.0.1:8000/api'

def get_categorias():
    response = requests.get(f'{URL_API}/categorias')
    return response.json()

def get_livros():
    response = requests.get(f'{URL_API}/livros')
    return response.json()
