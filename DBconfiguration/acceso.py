import psycopg2
import getpass #vuelve invisible en pantalla un input

# Configuración de conexión a la base de datos en Docker
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credenciales"
DB_USER = 'Admin'
DB_PASSWORD = "p4ssw0rdDB"

def conectar_db():
    """Conecta a la base de datos PostgreSQL y retorna la conexión."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None


def obtener_datos_usuario(username, password):
    #Consulta la base de datos para obtener los datos de un usuario a partir de sus credenciales.
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # Verificar si el usuario y contraseña existen en la tabla credenciales
        query = """
        SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
        FROM credenciales c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.username = %s AND c.password_hash = %s;
        """
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()

        if usuario:
            print("\nDatos del usuario encontrado:")
            print(f"ID: {usuario[0]}")
            print(f"Nombre: {usuario[1]}")
            print(f"Correo: {usuario[2]}")
            print(f"Teléfono: {usuario[3]}")
            print(f"Fecha de Nacimiento: {usuario[4]}")
            cursor.close()
            conn.close()
        else:
            print("\nUsuario o contraseña incorrectos.")
            cursor.close()
            conn.close()
    except Exception as e:
        print("Error al consultar la base de datos:", e)


def insertar_usuario(nombre, correo, telefono, fecha_nacimiento, username, password):
    conn = conectar_db()
    #condicion si no se conecta no sigue con el procedimiento
    if not conn:
        return
    
    try:
        #Crear el cursor
        cursor = conn.cursor() 
        #Insertar usuario en la tabla
        cursor.execute(
            """
            INSERT INTO usuarios(nombre, correo, telefono, fecha_nacimiento)
            VALUES (%s,%s,%s,%s) RETURNING id_usuario;
            """,(nombre,correo,telefono,fecha_nacimiento))

        # Guardamos el id del nuevo usuario
        id_usuario = cursor.fetchone()[0]

        #Guardamos el las nuevas credenciales del usuario
        cursor.execute(
            """
            INSERT INTO credenciales(id_usuario, username, password_hash)
            VALUES (%s,%s,%s);
            """,(id_usuario, username, password))
        
        #Confirmamos que los datos se guardaron correctamente
        conn.commit()
        print("Los datos del usuario se guardaron correctamente")

    #Si ahi un error manda el mensaje 
    except Exception as e:
        print("Error al insertar: ",e)

        #Revierte cualquier cambio, no guarda nada
        conn.rollback()
    finally:
        cursor.close()
        conn.close()            

def actualizar_correo(id_usuario, nuevo_correo):
    conn = conectar_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        #Actualizamos 
        cursor.execute("UPDATE usuarios SET correo = %s WHERE id_usuario = %s"), (nuevo_correo, id_usuario)

        #Se ejectan los cambios
        conn.commit()
        print("El correo se actualio correctamente")

    except Exception as e:
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
            

if __name__ == "__main__":
    print("Inicio de sesión en la base de datos")
    # Solicitar credenciales al usuario
    user = input("Ingrese su usuario: ")
    pwd = getpass.getpass("Ingrese su contraseña: ")#No muestra la contraseña a escribir
    #Consultar base de datos
    obtener_datos_usuario(user, pwd)
    print ("Modulo de actualizacion de correo")
    id_usuario = input ("Ingresa el id de usuario al que deseas actualizar")

