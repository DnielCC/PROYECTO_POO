import mysql.connector 

# Instalar >> pip install mysql-connector-python

class ConexionDB():
    def __init__(self):  
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='123456789', #Agregar password 
                database='bolsa_trabajo_2')
            self.cursor = self.connection.cursor()
            self.errMss = ''
        except Exception as ex:
            self.errMss = str(ex)  
            self.connection = None
            self.cursor = None

    def get_datos(self, query):
        if not self.connection:
            return []
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as ex:
            self.errMss = str(ex)  
            return []

    def insert_datos(self, query):
        if not self.connection:
            return "No hay conexión a la base de datos"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return 'ok'
        except Exception as ex:
            self.errMss = str(ex)
            return f"Error al insertar: {ex}"
    
    def update_datos(self, query):
        if not self.connection:
            return "No hay conexión a la base de datos"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return f"Registros actualizados: {self.cursor.rowcount}"
        except Exception as ex:
            self.errMss = str(ex)
            return f"Error al actualizar: {ex}"
    
    def delete_datos(self, query):
        if not self.connection:
            return "No hay conexión a la base de datos"
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return f"Registros eliminados: {self.cursor.rowcount}"
        except Exception as ex:
            self.errMss = str(ex)
            return f"Error al eliminar: {ex}"
    
    def get_datos_parametrizados(self, query, params=None):
        if not self.connection:
            return []
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as ex:
            self.errMss = str(ex)  
            return []
    
    def update_datos_parametrizados(self, query, params=None):
        if not self.connection:
            return "No hay conexión a la base de datos"
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return f"Registros actualizados: {self.cursor.rowcount}"
        except Exception as ex:
            self.errMss = str(ex)
            return f"Error al actualizar: {ex}"
    
    def insert_datos_parametrizados(self, query, params=None):
        if not self.connection:
            return "No hay conexión a la base de datos"
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return 'ok'
        except Exception as ex:
            self.errMss = str(ex)
            return f"Error al insertar: {ex}"
    
