from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta' 

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="",          
        database="inventario_ventas" 
    )

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor()
    
    sql = """
    SELECT 
        p.id_producto, 
        p.nombre_producto, 
        p.precio, 
        p.stock, 
        c.nombre_categoria
    FROM Productos p
    JOIN Categorias c ON p.id_categoria = c.id_categoria
    ORDER BY p.nombre_producto;
    """
    cursor.execute(sql)
    productos = cursor.fetchall() 
    cursor.close()
    db.close()
    
    return render_template('index.html', productos=productos)

@app.route('/add')
def add_product():
    return "Formulario para agregar productos (FASE 3)"

if __name__ == '__main__':
    app.run(debug=True)