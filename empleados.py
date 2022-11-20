import sqlite3

class Empleados:
    def __init__(self, clave, nombre, empleado, imagen):
        self.clave = clave
        self.nombre = nombre
        self.empleado = empleado
        self.imagen = imagen


class Registro:
    def __init__(self, clave: str, nombre: str, fecha: str, hora: str, imagen: str):
        self.clave = clave
        self.nombre = nombre
        self.fecha = fecha
        self.hora = hora
        self.imagen = imagen

__conn = None

def __abrirCon():
    global __conn
    __conn = sqlite3.connect('roots/empleados.bd')
    c = __conn.cursor()
    return c

def __cerrarCon():
    global __conn
    __conn.commit()
    __conn.close()


#############################################
#############################################
#############################################
######CORRER ESTO SOLO LA PRIMERA VEZ########
#############################################
#############################################
def ejecucionInicial():
    c = __abrirCon()
    c.execute("""
      CREATE TABLE IF NOT EXISTS EMPLEADOS (
        CLAVE TEXT PRIMARY KEY,
        NOMBRE TEXT,
        EMPLEADO INTEGER,
        IMAGEN TEXT
      )
    """)
    c.execute("""
      CREATE TABLE IF NOT EXISTS REGISTROS (
        CLAVE TEXT,
        NOMBRE TEXT,
        FECHA TEXT,
        HORA TEXT,
        IMAGEN TEXT
      )
    """)
    ##################### ACA EN VALUES IRIA CON SUS DATOS
    ##################### 0 - ES EMPLEADO, 1 - CRIMINAL, 2 - DESCONOCIDO
    c.execute("INSERT INTO EMPLEADOS VALUES('123','RAMIRO', 0, 'image/123.jpg')")
    __cerrarCon()
  
#ejecucionInicial()


############################################
############################################
#################### BD ####################
############################################
############################################
#   CREATE TABLE IF NOT EXISTS EMPLEADOS (
#     CLAVE TEXT PRIMARY KEY,
#     NOMBRE TEXT,
#     EMPLEADO INTEGER,
#     IMAGEN TEXT
#   )
# 
#   CREATE TABLE IF NOT EXISTS REGISTROS (
#     CLAVE TEXT,
#     NOMBRE TEXT,
#     FECHA TEXT,
#     HORA TEXT,
#     IMAGEN TEXT
#   )

def consultaClave(clave):
    c = __abrirCon()
    jeje = (clave,)
    c.execute("select * from EMPLEADOS where clave = ?", jeje)
    aux = c.fetchone()
    emp = Empleados(clave=aux[0], nombre=aux[1], empleado=aux[2], imagen=aux[3])
    __cerrarCon()
    return emp

def consultaEmpleadosClave(empleado):
    c = __abrirCon()
    aux = (empleado,)
    c.execute("select * from EMPLEADOS where EMPLEADO = ?", aux)
    emp = c.fetchall()
    __cerrarCon()
    return emp


def insertarEmp(empleado: Empleados):
    c = __abrirCon()
    c.execute("INSERT INTO EMPLEADOS VALUES(?, ?, ?, ?)", (empleado.clave, empleado.nombre, empleado.empleado, empleado.imagen))
    __cerrarCon()

  
def insertarRegistro(registro: Registro):
    c = __abrirCon()
    c.execute("INSERT INTO REGISTROS VALUES(?, ?, ?, ?, ?)", (registro.clave, registro.nombre, registro.fecha, registro.hora, registro.imagen))
    __cerrarCon()


def consultaRegistros():
    c = __abrirCon()
    c.execute("SELECT * FROM REGISTROS")
    aux = c.fetchall()
    __cerrarCon()
    return aux

def consultaRegistrosFecha(fecha: str):
    c = __abrirCon()
    fec = (fecha,)
    c.execute("SELECT * FROM REGISTROS where FECHA = ?", fec)
    aux = c.fetchall()
    __cerrarCon()
    return aux

def consulta(consulta):
    c = __abrirCon()
    c.execute(consulta)
    aux = c.fetchall()
    __cerrarCon()
    return aux
