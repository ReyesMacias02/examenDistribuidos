import socket
import psycopg2
import threading

# Configuración de la base de datos
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'Distribuidos'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

# Configuración del socket
HOST = '127.0.0.1'
PORT = 60080
BUFFER_SIZE = 1024

# Conexión a la base de datos
conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
cursor = conn.cursor()

# Crear socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

print('Iniciando el servidor en {} puerto {}'.format(HOST, PORT))


def consultar_datos(cedula):
    # Bloquear la fila del cliente
    cursor.execute('SELECT * FROM "User" WHERE "User"."idn" = %s FOR UPDATE', (cedula,))

    # Consultar la base de datos
    cursor.execute('SELECT "User"."Apellidos", "User"."Nombres", "User"."Saldo" FROM "User" WHERE "User"."idn" = %s', (cedula,))
    result = cursor.fetchone()
    return result


def actualizar_saldo(cedula, nuevo_saldo):
    # Bloquear la fila del cliente
    cursor.execute('SELECT * FROM "User" WHERE "User"."idn" = %s FOR UPDATE', (cedula,))

    # Actualizar el saldo en la base de datos
    cursor.execute('UPDATE "User" SET "Saldo" = %s WHERE "idn" = %s', (nuevo_saldo, cedula))
    conn.commit()


def handle_connection(connection):
    try:
        while True:
            print('-------------------------------')
            data = connection.recv(BUFFER_SIZE)
            print('Recibiendo dato: {!r}'.format(data))

            if not data:
                break

            # Decodificar los datos recibidos
            cedula, accion, nuevo_saldo = data.decode().split(',')

            if accion == 'consultar':
                # Consultar los datos de un cliente
                result = consultar_datos(cedula)

                if result:
                    apellidos, nombres, saldo = result
                    response = f"Apellidos: {apellidos}, Nombres: {nombres}, Saldo: {saldo}"
                else:
                    response = "No se encontró información para la cédula proporcionada"
            elif accion == 'actualizar':
                # Actualizar el saldo de un cliente
                actualizar_saldo(cedula, nuevo_saldo)
                response = f"Saldo actualizado para la cédula {cedula}"
            else:
                response = "Acción inválida"

            # Enviar respuesta al cliente
            connection.sendall(response.encode())
    finally:
        # Cerrar la conexión
        connection.close()


def accept_connections():
    while True:
        # Esperar conexión del cliente
        print('Esperando conexión de un cliente')
        connection, client_address = sock.accept()

        print('Conectado desde', client_address)

        # Manejar la conexión en un hilo separado
        thread = threading.Thread(target=handle_connection, args=(connection,))
        thread.start()


# Iniciar el hilo para aceptar conexiones
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Esperar a que el hilo de aceptar conexiones termine (Ctrl+C para detener el servidor)
accept_thread.join()

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()