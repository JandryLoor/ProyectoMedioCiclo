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

@app.route('/edit/<int:id_producto>')
def get_product(id_producto):
    categorias = get_categorias() 
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    sql = "SELECT * FROM Productos WHERE id_producto = %s"
    cursor.execute(sql, (id_producto,))
    producto = cursor.fetchone() 
    
    cursor.close()
    db.close()
    
    if producto is None:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('index'))
    
    return render_template('edit_product.html', producto=producto, categorias=categorias)

@app.route('/update/<int:id_producto>', methods=['POST'])
def update_product(id_producto):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        id_categoria = request.form['categoria']

        try:
            db = get_db_connection()
            cursor = db.cursor()
            
            sql = """
            UPDATE Productos 
            SET nombre_producto = %s, descripcion = %s, precio = %s, stock = %s, id_categoria = %s 
            WHERE id_producto = %s
            """
            data = (nombre, descripcion, precio, stock, id_categoria, id_producto)
            cursor.execute(sql, data)
            
            db.commit() 
            flash('Producto actualizado correctamente.', 'success')
            
            cursor.close()
            db.close()
        
        except mysql.connector.Error as err:
            flash(f"Error al actualizar: {err}", 'danger')
            
        return redirect(url_for('index'))

@app.route('/delete/<int:id_producto>')
def delete_product(id_producto):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        sql = "DELETE FROM Detalle_Pedido WHERE id_producto = %s" 
        cursor.execute(sql, (id_producto,))
  
        sql = "DELETE FROM Productos WHERE id_producto = %s"
        cursor.execute(sql, (id_producto,))
        
        db.commit()
        flash('Producto eliminado correctamente.', 'success')
        
        cursor.close()
        db.close()
        
    except mysql.connector.Error as err:
        flash(f"Error al eliminar: {err}", 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)