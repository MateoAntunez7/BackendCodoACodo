# Imports.
import os
from flask import Flask, jsonify, request, render_template, redirect, session, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "codo-a-codo-2023"

# Página de inicio
@app.route('/')
def index():
    if 'logged_in' in session:
        all_mangas = Manga.query.all()
        return render_template("index.html", mangas=all_mangas)
    else:
        return redirect(url_for('login'))

# Página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verificar las credenciales del usuario
        username = request.form['username']
        password = request.form['password']
        if username == 'codo' and password == 'codo':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)

# Página de cierre de sesión
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configurar base de datos.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/fireforcedatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Objetos de base de datos y marshmallow.
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Definir tablas de la base de datos.
class Manga(db.Model):
    # Campos de la tabla.
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    volumen = db.Column(db.Integer)
    imagen = db.Column(db.String(200))

    # Constructor de clase.
    def __init__(self, titulo, volumen, imagen):
        self.titulo = titulo
        self.volumen = volumen
        self.imagen = imagen

# Creación de tabla.
with app.app_context():
    db.create_all()

# Clase Esquemática de mangas.
class MangaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'titulo', 'volumen', 'imagen')

# Objetos de consulta de mangas.
manga_schema = MangaSchema()
mangas_schema = MangaSchema(many=True)

# Rutas de trabajo.
# Traer todos los mangas de la base de datos.
@app.route('/mangas', methods=['GET'])
def get_mangas():
    all_mangas = Manga.query.all()
    return mangas_schema.jsonify(all_mangas)

# Traer un solo manga.
@app.route("/mangas/<id>", methods=['GET'])
def get_manga(id):
    manga = Manga.query.get(id)
    return manga_schema.jsonify(manga)

# Eliminar un manga.
@app.route("/mangas/<int:id>", methods=['POST'])
def delete_manga(id):
    manga = Manga.query.get(id)
    db.session.delete(manga)
    db.session.commit()
    return redirect(url_for('index'))

# Cargar un manga.
app.config['STATIC_IMAGES'] = 'static/images'
app.static_folder = 'static'

@app.route("/mangas", methods=['POST'])
def create_manga():
    titulo = request.form['titulo']
    volumen = request.form['volumen']
    imagen = request.files['imagen']

    filename = secure_filename(imagen.filename)
    image_path = os.path.join("static/images/", filename)
    imagen.save(image_path)
    print(image_path)

    db_path_img = "http://127.0.0.1:5000/" + image_path   ###CAMBIAR PATH A HOST FINAL###
    nuevo_manga = Manga(titulo, volumen, db_path_img)
    db.session.add(nuevo_manga)
    db.session.commit()

    return redirect(url_for('index'))

# Modificar un manga.
@app.route("/mangas/<int:id>/edit", methods=['GET', 'POST'])
def edit_manga(id):
    manga = Manga.query.get(id)

    if request.method == 'POST':
        titulo = request.form['titulo']
        volumen = request.form['volumen']
        imagen = request.files['imagen']

        if imagen:
            # Guardar imagen en la carpeta de imágenes estáticas solo si se carga una nueva imagen.
            filename = secure_filename(imagen.filename)
            image_path = os.path.join("static/images/", filename)
            imagen.save(image_path)
            print(image_path)

            manga.imagen = "http://127.0.0.1:5000/" + image_path  ### CAMBIAR PATH A HOST FINAL ###

        manga.titulo = titulo
        manga.volumen = volumen

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit_manga.html', manga=manga)


if __name__ == '__main__':
    app.run(debug=True)
