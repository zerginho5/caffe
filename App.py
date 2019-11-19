from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_mysqldb import MySQL


import datetime
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'macho123'
app.config['MYSQL_DB'] = 'caffe'
mysql = MySQL(app)
app.secret_key = 'super secret key'
app.config.from_object(__name__)
SECRET_KEY = ('super secret key')

@app.route('/')
def principal():
    session['band'] = 0
    session['cant'] = [()]
    session['prod'] = []
    session['impo'] = []
    return render_template('inicio.html')


@app.route('/crear')
def crear():
    return render_template('crear.html')

@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    cur = mysql.connection.cursor()
    name = request.form['fullname']
    password = request.form['password']
    cur.execute('SELECT puesto FROM usuario WHERE nombre=%s and clave =%s', (name,password))
    data = cur.fetchall()
    cur.close()
    if len(data)==0:
        flash('Datos incorrectos, vuelva a intentarlo.')
        return redirect(url_for('principal'))
    else:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuario')
        data = cur.fetchall()
        session['usr']=name
        cur.close()
        return render_template('usuarios.html', contacts=data)

#Seccion
@app.route('/seccion')
def seccion():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM seccion')
    data = cur.fetchall()
    cur.close()
    return render_template('seccion.html',  contacts = data)

@app.route('/add_sec', methods=['POST'])
def add_sec():
    if request.method == 'POST':
        fullname = request.form['fullname']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO seccion (nombre) VALUES (%s)", [fullname])
        mysql.connection.commit()
        flash('Seccion añadida correctamente')
        return redirect(url_for('seccion'))

@app.route('/editsec/<id>', methods = ['POST', 'GET'])
def get_sec(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM seccion WHERE idseccion = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-seccion.html', contact = data[0])

@app.route('/updatesec/<id>', methods=['POST'])
def update_sec(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE seccion SET nombre = %s WHERE idseccion = %s', (fullname, id))
        flash('Seccion modificada correctamente')
        mysql.connection.commit()
        return redirect(url_for('seccion'))

@app.route('/deletesec/<string:id>', methods = ['POST','GET'])
def delete_sec(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM seccion WHERE idseccion = {0}'.format(id))
    mysql.connection.commit()
    flash('Seccion removida correctamente')
    return redirect(url_for('seccion'))

#Categoria
@app.route('/categoria')
def categoria():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoria')
    data = cur.fetchall()
    cur.close()
    return render_template('categoria.html',  contacts = data)

@app.route('/add_cat', methods=['POST'])
def add_cat():
    if request.method == 'POST':
        fullname = request.form['fullname']
        descripcion = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO categoria (nombre, descripcion) VALUES (%s,%s)", (fullname,descripcion))
        mysql.connection.commit()
        flash('Categoria añadida correctamente')
        return redirect(url_for('categoria'))

@app.route('/editcat/<id>', methods = ['POST', 'GET'])
def get_cat(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM categoria WHERE idcategoria = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-categoria.html', contact = data[0])

@app.route('/updatecat/<id>', methods=['POST'])
def update_cat(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE categoria
            SET nombre = %s,
                descripcion = %s
            WHERE idcategoria = %s
        """, (fullname, descripcion, id))
        flash('Categoria modificada correctamente')
        mysql.connection.commit()
        return redirect(url_for('categoria'))

@app.route('/deletecat/<string:id>', methods = ['POST','GET'])
def delete_cat(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM categoria WHERE idcategoria = {0}'.format(id))
    mysql.connection.commit()
    flash('Categoria removida correctamente')
    return redirect(url_for('categoria'))

#usuarios
@app.route('/usuarios')
def usuario():

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario')
    data = cur.fetchall()
    cur.close()
    session['band'] = 0
    return render_template('usuarios.html',  contacts = data)

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        password = request.form['password']
        email = request.form['email']
        sexo = request.form['sexo']
        puesto = request.form['puesto']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (nombre, telefono,clave,email,sexo,puesto) VALUES (%s,%s,%s,%s,%s,%s)", (fullname, phone,password, email,sexo,puesto))
        mysql.connection.commit()
        flash('Usuario añadido correctamente')
        return redirect(url_for('usuario'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE idusuario = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-usuario.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        password = request.form['password']
        email = request.form['email']
        sexo = request.form['sexo']
        puesto = request.form['puesto']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuario
            SET nombre = %s,
                telefono = %s,
                clave = %s,
                email = %s,
                sexo = %s,
                puesto = %s
            WHERE idusuario = %s
        """, (fullname, phone,password, email,sexo,puesto, id))
        flash('Usuario modificado correctamente')
        mysql.connection.commit()
        return redirect(url_for('usuario'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuario WHERE idusuario = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario removido correctamente')
    return redirect(url_for('usuario'))

#Punto de venta

@app.route('/punto')
def punto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto')
    data = cur.fetchall()
    cur.close()
    cant1 = session['cant'].copy()
    prod1 = session['prod'].copy()
    impo1 = session['impo'].copy()
    session['band']=1
    return render_template('punto.html',  contacts = data, can=cant1, pro=prod1, imp=impo1)

@app.route('/add_pt', methods = ['POST','GET'])
def add_pt():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto')
    data1 = cur.fetchall()
    cur.close()
    cantidad = float(request.form['cantidad'])
    producto = request.form['producto']
    cur = mysql.connection.cursor()
    cur.execute('SELECT precio FROM producto WHERE idproducto = {0}'.format(producto))
    data = cur.fetchall()
    precio  = [x[0] for x in data]
    importe = (cantidad)*precio[0]
    cant1 = [(importe,cantidad,producto)]
    prod1 = [producto]
    impo1 = [importe]
    cant1 = cant1 + session['cant']
    prod1 = prod1 + session['prod']
    impo1 = impo1 + session['impo']
    session['cant']=cant1
    session['prod'] = prod1
    session['impo'] = impo1
    print(cant1)
    print(prod1)
    print(impo1)
    return render_template('punto.html',  contacts = data1, can=cant1, pro=prod1, imp=impo1)


@app.route('/add_gpt', methods=['POST'])
def add_gpt():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('SELECT idusuario FROM usuario WHERE nombre={0}'.format(session['usr']))
        usr=cur.fetchall()
        total=0
        usuario = [x[0] for x in usr]
        for im in session['cantidad']:
            total=total+im[0]

        cur.execute('INSERT INTO venta (importe,fecha,idusuario)',(total,datetime.datetime.now(),usuario))
        for im in session['cantidad']:
            cur.execute('INSERT INTO ventaproducto (importe,cantidad,idproducto,idventa) VALUES', (im[0], im[1], im[2]))


        mysql.connection.commit()
        flash('Venta añadida. Importe cobrar={0}'.format(total))
        return redirect(url_for('producto'))
#Producto
@app.route('/producto')
def producto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto')
    data = cur.fetchall()
    cur.execute('SELECT * FROM seccion')
    data1 = cur.fetchall()
    cur.execute('SELECT * FROM categoria')
    data2 = cur.fetchall()
    cur.close()
    return render_template('producto.html',  contacts = data,sec=data1,cat=data2)




@app.route('/add_prod', methods=['POST'])
def add_prod():
    if request.method == 'POST':
        fullname = request.form['fullname']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        existencias = request.form['existencias']
        seccion = request.form['seccion']
        categoria = request.form['categoria']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO producto (nombre, precio,descripcion,existencias,idseccion,idcategoria) VALUES (%s,%s,%s,%s,%s,%s)",
                    (fullname, precio,descripcion, existencias,seccion,categoria))
        mysql.connection.commit()
        flash('Producto añadido correctamente')
        return redirect(url_for('producto'))

@app.route('/editprod/<id>', methods = ['POST', 'GET'])
def get_prod(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE idproducto = %s', (id))
    data = cur.fetchall()
    cur.execute('SELECT * FROM seccion')
    data1 = cur.fetchall()
    cur.execute('SELECT * FROM categoria')
    data2 = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-producto.html', contact = data[0],sec=data1,cat=data2)

@app.route('/updateprod/<id>', methods=['POST'])
def update_prod(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        existencias = request.form['existencias']
        seccion = request.form['seccion']
        categoria = request.form['categoria']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE producto
            SET nombre = %s,
                precio = %s,
                descripcion = %s,
                existencias = %s,
                idseccion = %s,
                idcategoria = %s
            WHERE idproducto = %s
        """, (fullname, precio,descripcion, existencias,seccion,categoria, id))
        flash('Producto modificado correctamente')
        mysql.connection.commit()
        return redirect(url_for('producto'))

@app.route('/deleteprod/<string:id>', methods = ['POST','GET'])
def delete_prod(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM producto WHERE idproducto = {0}'.format(id))
    mysql.connection.commit()
    flash('Producto removido correctamente')
    return redirect(url_for('producto'))
#Ventas
@app.route('/venta')
def venta():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM venta')
    data = cur.fetchall()
    cur.execute('SELECT * FROM usuario')
    data1 = cur.fetchall()
    cur.execute('SELECT * FROM producto')
    data2 = cur.fetchall()
    cur.close()
    return render_template('producto.html',  contacts = data,usr=data1,prod=data2)

@app.route('/add_vent', methods=['POST'])
def add_vent():
    if request.method == 'POST':
        cantidad = request.form['cantidad']
        fecha = request.form['fecha']
        producto = request.form['producto']
        usuario = request.form['usuario']
        cur = mysql.connection.cursor()
        data=cur.execute('SELECT precio FROM producto WHERE nombre=%s',[producto])
        importe=float(data)*int(cantidad)
        cur.execute("INSERT INTO venta (cantidad, importe,fecha,idproducto,idusuario) VALUES (%s,%s,%s,%s,%s)", (cantidad, importe,fecha, producto,usuario))
        mysql.connection.commit()
        flash('Venta añadida correctamente')
        return redirect(url_for('producto'))

@app.route('/editvent/<id>', methods = ['POST', 'GET'])
def get_vent(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE idproducto = %s', (id))
    data = cur.fetchall()
    cur.execute('SELECT * FROM seccion')
    data1 = cur.fetchall()
    cur.execute('SELECT * FROM categoria')
    data2 = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-producto.html', contact = data[0],sec=data1,cat=data2)

@app.route('/updatevent/<id>', methods=['POST'])
def update_vent(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        existencias = request.form['existencias']
        seccion = request.form['seccion']
        categoria = request.form['categoria']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE producto
            SET nombre = %s,
                precio = %s,
                descripcion = %s,
                existencias = %s,
                idseccion = %s,
                idcategoria = %s
            WHERE idproducto = %s
        """, (fullname, precio,descripcion, existencias,seccion,categoria, id))
        flash('Producto modificado correctamente')
        mysql.connection.commit()
        return redirect(url_for('producto'))

@app.route('/deletevent/<string:id>', methods = ['POST','GET'])
def delete_vent(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM venta WHERE idventa = {0}'.format(id))
    mysql.connection.commit()
    flash('Venta removida correctamente')
    return redirect(url_for('venta'))

# starting the app
if __name__ == "__main__":

    app.run(port=3000, debug=True)
