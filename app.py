from flask import Flask, request, jsonify
import mysql.connector
from urllib.parse import urlparse

app = Flask(__name__)

# Configuración de MySQL utilizando la URL pública
db_url = 'mysql://root:goOoewyPEWbzNShkUasUkUtVmILFOKmY@autorack.proxy.rlwy.net:56107/railway'

# Parsear la URL para obtener los componentes de la base de datos
url = urlparse(db_url)
db_config = {
    'host': url.hostname,
    'port': url.port,
    'user': url.username,
    'password': url.password,
    'database': url.path[1:],  # Eliminar el primer carácter '/'
}

# Ruta para recibir datos del ESP32
@app.route('/sensores', methods=['POST'])
def recibir_datos():
    # Obtener los datos del cuerpo de la solicitud en formato JSON
    data = request.get_json()
    temperatura = data.get('temperatura')
    humedad = data.get('humedad')

    # Conectar a MySQL
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insertar los datos en la tabla
        query = "INSERT INTO sensores (temperatura, humedad) VALUES (%s, %s)"
        cursor.execute(query, (temperatura, humedad))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'message': 'Datos insertados correctamente'}), 200
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({'error': str(err)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
