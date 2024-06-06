from flask import Blueprint, jsonify, request

# Route principale
books_bp = Blueprint('books', __name__)

# Base de données interne
books = [
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
    }
]

# Requete pour toutes les données
@books_bp.route('/', methods=['GET'])
def get_books():
    return jsonify(books)

# Recherche par titre
@books_bp.route('/title/<string:book_title>', methods=['GET'])
def get_book_title(book_title):
    # Liste des résultats
    result = [book for book in books if book['title'] == book_title]
    # Renvoie une erreur en cas de liste vide
    if not result:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(result)

# Recherche par auteur
@books_bp.route('/author/<string:book_author>', methods=['GET'])
def get_book_author(book_author):
    # Liste des résultats
    result = [book for book in books if book['author'] == book_author]
    # Renvoie une erreur en cas de liste vide
    if not result:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(result)

@books_bp.route('/', methods=['POST'])
def add_book():
    # Récupère les informations des champs
    new_book = request.get_json()
    # Vérification de la présence des éléments nécessaires
    required_fields = ['id', 'title', 'author', 'published']
    for field in required_fields:
        # Renvoie une erreur en cas de champs vides
        if field not in new_book:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # Vérification du type des champs
    if not isinstance(new_book['id'], int) or not isinstance(new_book['title'], str) or \
       not isinstance(new_book['author'], str) or not isinstance(new_book['published'], str):
        return jsonify({'error': 'Invalid data types'}), 400

    # Vérification de l'unicité de l'ID
    if any(book['id'] == new_book['id'] for book in books):
        return jsonify({'error': 'Book with this ID already exists'}), 400

    # Ajout du nouvel élément
    books.append(new_book)
    return jsonify(new_book), 201

@books_bp.route('/<int:book_id>',methods=['DELETE'])
def remove_book(book_id):
    # Recherche le livre avec le bon id
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return jsonify({'message': 'Book removed'}), 200
    # Renvoie une erreur
    return jsonify({'error': 'Book not found'}), 404

@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    # Recherche le livre avec le bon id
    for book in books:
        if book['id'] == book_id:
            # Récupère les informations des champs
            new_book = request.get_json()
            # Récupère les éléments si tous les champs ne sont pas renseignés
            for key, value in book.items():
                if key not in new_book or new_book[key] == "":
                    new_book[key] = value

            # Mise à jour
            book.update(new_book)
            return jsonify(book)
    # Renvoie une erreur
    return jsonify({'error': 'Book not found'}), 404