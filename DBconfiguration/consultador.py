import psycopg2

conexion = psycopg2.connect(
    host = "localhost",
    port = "5432",
    database ="credenciales",
    user = "Admin",
    password ="p4ssw0rdDB"
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM usuarios")
registros = cursor.fetchall()

for fila in registros
    print(fila)
    
#cerrar conexion
cursor.close()
conexion.close()

