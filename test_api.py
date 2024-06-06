import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Teste get_books
def test_get_books(client):
    response = client.get('/books/')
    assert response.status_code == 200
    assert response.json == [
        {
        'id': 1,
        'title': '1984',
        'author': 'George Orwell',
        'published': 1949
    },
        {
        'id': 2,
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'published': 1960
    }]

# Teste get_book par titre 
def test_get_book_title(client):
    response = client.get('/books/title/To%20Kill%20a%20Mockingbird')
    assert response.status_code == 200
    assert response.json == [
        {
        'id': 2,
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'published': 1960
    }]

# Teste get_book par titre en cas d'erreur
def test_get_book_title_404(client):
    response = client.get('/books/title/Hello')
    assert response.status_code == 404
    assert response.json == {'error': 'Book not found'}

# Teste get_book par auteur
def test_get_book_author(client):
    response = client.get('/books/author/George%20Orwell')
    assert response.status_code == 200
    assert response.json == [
        {
        'id': 1,
        'title': '1984',
        'author': 'George Orwell',
        'published': 1949
    }]

# Teste get_book par auteur en cas d'erreur
def test_get_book_author_404(client):
    response = client.get('/books/author/Hello')
    assert response.status_code == 404
    assert response.json == {'error': 'Book not found'}

# Teste add_book si pas le bon nombre de champs
def test_add_book_fields(client):
    new_book = {
        'id': 3,
        'title': '1984',
        'author': 'George Orwell'
    }
    response = client.post('/books/', json=new_book)
    assert response.status_code == 400
    assert response.json == {'error': 'Missing field: published'}

# Teste add_book si pas le bon type de variables
def test_add_book_types(client):
    new_book = {
        'id': 'three',
        'title': '1984',
        'author': 'George Orwell',
        'published': 1949
    }
    response = client.post('/books/', json=new_book)
    assert response.status_code == 400
    assert response.json == {'error':'Invalid data types'}

# Teste add_book si id en doublon
def test_add_book_id(client):
    new_book = {
        'id': 1,
        'title': '1984',
        'author': 'George Orwell',
        'published': 1949
    }
    response = client.post('/books/', json=new_book)
    assert response.status_code == 400
    assert response.json == {'error':'Book with this ID already exists'}

# Teste add_book sans erreur
def test_add_book(client):
    new_book = {
        'id': 3,
        'title': '1985',
        'author': 'Georges Orwell',
        'published': 1950
    }
    response = client.post('/books/', json=new_book)
    assert response.status_code == 201
    assert response.json == {'id': 3,
        'title': '1985',
        'author': 'Georges Orwell',
        'published': 1950}

# Teste remove_book
def test_remove_book(client):
    response = client.delete('/books/1')
    assert response.status_code == 200
    assert response.json == {'message': 'Book removed'}

# Teste remove_book avec erreur d'id
def test_remove_book_false(client):
    response = client.delete('/books/999')
    assert response.status_code == 404
    assert response.json == {'error': 'Book not found'}

# Teste update_book
def test_update_book(client):
    response = client.put('/books/3',json={'id': 3,
        'title': 'modif',
        'author': 'Moi',
        'published': 2024})
    assert response.status_code == 200
    assert response.json == {'id': 3,
        'title': 'modif',
        'author': 'Moi',
        'published': 2024}

# Teste update_book avec erreur id
def test_update_book_false(client):
    response = client.put('/books/999',json={'id': 999,
        'title': 'modif',
        'author': 'Moi',
        'published': 2024})
    assert response.status_code == 404
    assert response.json == {'error': 'Book not found'}