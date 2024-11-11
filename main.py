from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
import pandas as pd

app = Flask(__name__)
CORS(app)

DATABASE = 'movie_recommendations.db'

# Cargar datos en una tabla simplificada de SQLite
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Crear tabla única que almacene toda la información relevante
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                        UserID INTEGER,
                        MovieID INTEGER,
                        Title TEXT,
                        Rating INTEGER,
                        Timestamp INTEGER,
                        Genres TEXT,
                        Gender TEXT,
                        Age INTEGER,
                        Occupation INTEGER,
                        ZipCode TEXT
                      )''')

    # Cargar y fusionar datos de los CSV
    movies_df = pd.read_csv(
        'ml-1m/movies_cleaned.csv', 
        encoding='ISO-8859-1', 
        delimiter=',', 
        header=None, 
        names=['MovieID', 'Title', 'Genres'],
        on_bad_lines='skip'  # Omitir filas con errores
    )
    ratings_df = pd.read_csv(
        'ml-1m/ratings_cleaned.csv', 
        encoding='ISO-8859-1', 
        delimiter=',', 
        header=None, 
        names=['UserID', 'MovieID', 'Rating', 'Timestamp']
    )
    users_df = pd.read_csv(
        'ml-1m/users_cleaned.csv', 
        encoding='ISO-8859-1', 
        delimiter=',', 
        header=None, 
        names=['UserID', 'Gender', 'Age', 'Occupation', 'ZipCode']
    )

    # Fusionar los datos en un único DataFrame
    merged_df = ratings_df.merge(movies_df, on="MovieID", how="left").merge(users_df, on="UserID", how="left")
    
    # Insertar los datos en la tabla SQLite
    merged_df.to_sql('data', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()


# Inicializar la base de datos al iniciar la aplicación
init_db()

# Ruta principal para mostrar la interfaz HTML y procesar votos
@app.route("/", methods=["GET", "POST"])
def index():
    # Valores de opciones de votación
    option_a = "Película A"
    option_b = "Película B"
    hostname = request.host  # ID del contenedor o nombre del host

    # Procesar el voto si se envía
    vote = None
    if request.method == "POST":
        vote = request.form.get("vote")

    # Ejemplo de recomendaciones, normalmente vendrían de tu base de datos
    recommendations = [
        {"MovieID": 1, "Title": "Toy Story", "Rating": 4.5},
        {"MovieID": 2, "Title": "Inception", "Rating": 4.7}
    ]

    return render_template("index.html", option_a=option_a, option_b=option_b, hostname=hostname, vote=vote, recommendations=recommendations)

# Endpoint para obtener los datos
@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data LIMIT 10")  # Obtener las primeras 10 filas como ejemplo
    rows = cursor.fetchall()
    conn.close()

    # Convertir a formato JSON
    data_list = [{
        "UserID": row[0],
        "MovieID": row[1],
        "Title": row[2],
        "Rating": row[3],
        "Timestamp": row[4],
        "Genres": row[5],
        "Gender": row[6],
        "Age": row[7],
        "Occupation": row[8],
        "ZipCode": row[9]
    } for row in rows]
    
    return jsonify(data_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
