from config import ConexionDB

def crear_usuario_reclutador():
    conexion = ConexionDB()
    
    # Datos del usuario reclutador
    email = "reclutador@workify.com"
    password = "reclutador123"
    tipo_usuario = "reclutador"
    
    # Verificar si el usuario ya existe
    consulta = conexion.get_datos(f"SELECT * FROM login WHERE correo = '{email}'")
    
    if len(consulta) > 0:
        print(f"El usuario {email} ya existe en la base de datos.")
        return
    
    # Insertar el usuario reclutador
    resultado = conexion.insert_datos(
        f"INSERT INTO login (correo, contra, tipo_usuario) VALUES ('{email}', '{password}', '{tipo_usuario}')"
    )
    
    if resultado == 'ok':
        print(f"Usuario reclutador creado exitosamente:")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Tipo: {tipo_usuario}")
        print("\nPuedes usar estas credenciales para acceder al módulo de reclutador.")
    else:
        print(f"Error al crear el usuario reclutador: {resultado}")

if __name__ == "__main__":
    crear_usuario_reclutador() 