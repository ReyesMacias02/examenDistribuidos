import socket
from tabulate import tabulate
# Configuración del servidor
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 60080
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

def main_menu():
    # Menú principal
    print('Bienvenido al sistema de consulta y actualización de saldos')
    print('1. Consultar información de un cliente')
    print('2. Agregar saldo a un cliente')
    print('0. Salir')

def consultar_cliente():
    # Consultar información de un cliente
    cedula = input('Ingrese la cédula del cliente: ')
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
        print(table)
    else:
        print(response)
def agregar_saldo():
    # Agregar saldo a un cliente
    cedula = input('Ingrese la cédula del cliente: ')
    saldo = input('Ingrese el saldo a agregar: ')
    accion='actualizar'
    data = cedula + ',' + accion + ',' + saldo
    send_request(data)
    response = receive_response()
    print('Respuesta del servidor:')
    print(response)

# Conectar al servidor
connect_to_server()

while True:
    main_menu()
    opcion = input('Seleccione una opción: ')

    if opcion == '1':
        consultar_cliente()
    elif opcion == '2':
        agregar_saldo()
    elif opcion == '0':
        break
    else:
        print('Opción inválida. Intente nuevamente.')

# Cerrar la conexión
close_connection()