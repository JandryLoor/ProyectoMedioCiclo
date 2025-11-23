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

def get_categorias():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True) 
    cursor.execute("SELECT id_categoria, nombre_categoria FROM Categorias")
    categorias = cursor.fetchall()
    cursor.close()
    db.close()
    return categorias


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

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        id_categoria = request.form['categoria']

        try:
            db = get_db_connection()
            cursor = db.cursor()
            
            sql = "INSERT INTO Productos (nombre_producto, descripcion, precio, stock, id_categoria) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nombre, descripcion, precio, stock, id_categoria))
            
            db.commit()
            flash('Producto agregado exitosamente.', 'success')
            
            cursor.close()
            db.close()
            
            return redirect(url_for('index'))
            
        except mysql.connector.Error as err:
            flash(f"Error al agregar producto: {err}", 'danger')
            return redirect(url_for('add_product'))

    categorias = get_categorias()
    return render_template('add_product.html', categorias=categorias)


if __name__ == '__main__':
    app.run(debug=True)