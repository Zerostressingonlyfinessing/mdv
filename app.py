from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models import db, Product
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
app.config['SECRET_KEY'] = 'verysecretkey'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/admin')
def admin():
    products = Product.query.all()
    return render_template('admin/dashboard.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        material = request.form['material']
        price = request.form['price']
        images = request.files.getlist('images')

        filenames = []
        for image in images:
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(path)
                filenames.append(filename)

        product = Product(
            name=name,
            description=description,
            category=category,
            material=material,
            price=price,
            images=filenames
        )
        db.session.add(product)
        db.session.commit()
        flash('Товар добавлен!', 'success')
        return redirect(url_for('admin'))

    return render_template('admin/add_product.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
