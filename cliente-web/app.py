from flask import Flask, render_template, request
from tabulate import tabulate
import socket

app = Flask(__name__)

# Configuración del servidor
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 60090
BUFFER_SIZE = 1024

# Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server():
    # Conectar al servidor
    print('Conectando al servidor {} puerto {}'.format(SERVER_HOST, SERVER_PORT))
    sock.connect((SERVER_HOST, SERVER_PORT))

def send_request(data):
    # Enviar solicitud al servidor
    sock.sendall(data.encode())

def receive_response():
    # Recibir respuesta del servidor
    response = sock.recv(BUFFER_SIZE).decode()
    return response

def close_connection():
    # Cerrar la conexión
    sock.close()

@app.route('/', methods=['GET', 'POST'])
def main_menu():
    if request.method == 'POST':
        opcion = request.form['opcion']
        if opcion == '1':
            return consultar_cliente()
        elif opcion == '2':
            return agregar_saldo()
        elif opcion == '0':
            close_connection()
            return '¡Hasta luego!'
        else:
            return 'Opción inválida. Intente nuevamente.'

    return render_template('index.html')
@app.route('/regresar')
def regresar():
     return render_template('index.html', )
def consultar_cliente():
    # Consultar información de un cliente
    cedula = request.form['cedula']
    accion='consultar'
    saldo='0'
    data = cedula + ',' + accion + ',' + saldo
    send_request(data)
    response = receive_response()

    if response.startswith("Apellidos:"):
        # Obtener los datos de la respuesta
        datos = response.split(':')
        apellidos = datos[1].strip().split(',')[0].strip()
        nombres = datos[2].strip().split(',')[0].strip()
        saldo = datos[3].strip().split(',')[0].strip()

        # Crear la tabla con los datos
        headers = ['Apellidos', 'Nombres', 'Saldo']
        data = [[apellidos, nombres, saldo]]
        table = tabulate(data, headers, tablefmt='grid')
        return render_template('tabla.html', data=data)
    else:
        return response

def agregar_saldo():
    # Agregar saldo a un cliente
    cedula = request.form['cedula']
    saldo = request.form['saldo']
    accion='actualizar'
    data = cedula + ',' + accion + ',' + saldo
    send_request(data)
    response = receive_response()
    return response

# Conectar al servidor
connect_to_server()

if __name__ == '__main__':
    app.run()
