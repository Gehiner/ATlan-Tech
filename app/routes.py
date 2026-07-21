from app.models import ItemPedido, Pedido, Producto
from flask_login import login_required
from app import db
from flask import  Blueprint, render_template, request, redirect, url_for, session


main = Blueprint('main', __name__)
@main.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@main.route('/admin')
@login_required
def admin():
    productos = Producto.query.all()
    return render_template('admin/admin.html', productos=productos)

@main.route('/admin/create', methods=['GET', "POST"])
@login_required
def create():
    if request.method == "POST":
        nombre=request.form['nombre']
        descripcion=request.form['descripcion']
        precio=request.form['precio']
        imagen=request.form['imagen']
        stock = request.form['stock']
        nuevo_producto = Producto(nombre=nombre, precio=precio, descripcion=descripcion, imagen=imagen, stock=stock)
        db.session.add(nuevo_producto)
        db.session.commit()
        return  redirect(url_for('main.admin'))
    else:
        return render_template('admin/create.html')

@main.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == "POST":
        producto=Producto.query.get_or_404(id)
        producto.nombre=request.form['nombre']
        producto.descripcion=request.form['descripcion']
        producto.precio=request.form['precio']
        producto.imagen=request.form['imagen']
        producto.stock = request.form['stock']
        db.session.commit()
        return  redirect(url_for('main.admin'))
    else:
        return render_template('admin/edit.html', producto=Producto.query.get_or_404(id))

@main.route('/admin/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    producto=Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return  redirect(url_for('main.admin'))

@main.route('/carrito/agregar/<int:id>', methods=['POST'])
def agregar_carrito(id):
    carrito = session.get('carrito', {})
    id_str = str(id)
    carrito[id_str] = carrito.get(id_str, 0) + 1
    session['carrito'] = carrito
    return redirect(url_for('main.index'))

@main.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    items = []
    total = 0
    for id_str, cantidad in carrito.items():
        producto = Producto.query.get(int(id_str))
        subtotal = producto.precio * cantidad
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
        total += subtotal
    return render_template('carrito.html', items=items, total=total)

@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    carrito = session.get('carrito', {})
    if not carrito:
        return redirect(url_for('main.ver_carrito'))

    if request.method == 'POST':
        nombre_cliente = request.form['nombre']
        email_cliente = request.form['email']
        direccion = request.form['direccion']

        nuevo_pedido = Pedido(nombre_cliente=nombre_cliente, email_cliente=email_cliente, direccion=direccion)
        db.session.add(nuevo_pedido)

        for id_str, cantidad in carrito.items():
            producto = Producto.query.get(int(id_str))
            item = ItemPedido(pedido=nuevo_pedido, producto_id=producto.id, cantidad=cantidad, precio_unitario=producto.precio)
            db.session.add(item)
            producto.stock -= cantidad

        db.session.commit()
        session.pop('carrito', None)
        return redirect(url_for('main.confirmacion', id=nuevo_pedido.id))
    else:
        return render_template('checkout.html')

@main.route('/confirmacion/<int:id>')
def confirmacion(id):
    pedido = Pedido.query.get_or_404(id)
    return render_template('confirmacion.html', pedido=pedido)

@main.route('/carrito/restar/<int:id>', methods=['POST'])
def restar_carrito(id):
    carrito = session.get('carrito', {})
    id_str = str(id)
    if id_str in carrito:
        carrito[id_str] -= 1
        if carrito[id_str] <= 0:
            del carrito[id_str]
    session['carrito'] = carrito
    return redirect(url_for('main.ver_carrito'))

@main.route('/carrito/agregar_mas/<int:id>', methods=['POST'])
def agregar_mas_al_carrito(id):
    carrito = session.get('carrito', {})
    id_str = str(id)
    carrito[id_str] = carrito.get(id_str, 0) + 1
    session['carrito'] = carrito
    return redirect(url_for('main.ver_carrito'))

