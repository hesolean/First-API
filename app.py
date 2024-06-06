from flask import Flask, render_template
from books import books_bp

app = Flask(__name__)

# Ignore requests for favicon.ico
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Enregistrer le blueprint des livres avec le préfixe /books
app.register_blueprint(books_bp, url_prefix='/books')

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
