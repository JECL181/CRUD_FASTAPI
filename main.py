import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel # BaseModel es una clase proporcionada por Pydantic
app = FastAPI() # Crea nuestra instancia de FastAPI
# Objeto para decir que una function será utilizada mediante HTTP

conexion = mysql.connector.connect(
    host= "localhost",
    user="root",
    password="",
    database="crud_practicas"
)
print("Conexion exitosa")

cursor = conexion.cursor()

class Producto(BaseModel): #hago que Producto herede de BaseModel
    # hago que sea un modelo de datos de PyDantic
    nombre: str
    precio: float
@app.post("/productos") # Registra la funcion como la encargada de lo que llegue del POST /productos
    # /productos es el endpoint que estamos creando
# --CREATE--
def crear(producto: Producto):
    query= """
    INSERT INTO productos(nombre, precio) VALUES(%s, %s) 
    """ # %s = marcador de parametro
    cursor.execute(query, (producto.nombre, producto.precio))
    conexion.commit()
    return {
        "mensaje": "Producto agregado"
    }
# --READ--
@app.get("/productos")
def obtener_productos():
    cursor.execute("""SELECT * FROM productos""")
    productos = cursor.fetchall() # Practicamente traer todos
    return productos

# Variacion del READ
@app.get("/productos{id}") # {} = Habrá un valor dentro de la URL
def obtener_producto(id: int):
    cursor.execute("""SELECT * FROM productos WHERE id = %s""", (id,)) # Una tupla que contiene el id
    return cursor.fetchone()

# --UPDATE--
@app.put("/productos{id}")
def modificar_producto(id:int, producto: Producto):
    query= """UPDATE productos SET nombre = %, precio = %s WHERE id = %s"""
    cursor.execute(query, (producto.nombre, producto.precio, id))
    conexion.commit()
    return {
        "mensaje": "producto modificado"
    }

# --DELETE--
@app.delete("/productos{id}")
def elimiar_producto(id:int):
    cursor.execute("""DELETE FROM Productos WHERE id= %s""", (id,))
    conexion.commit()
    return {
        "mensaje": "Producto Retirado"
    }


