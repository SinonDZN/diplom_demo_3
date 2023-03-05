from flask import Flask, render_template, url_for, request, redirect
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from flask_admin import Admin, BaseView, AdminIndexView, expose
#from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    info = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.Text, nullable=False)
    shortname = db.Column(db.Text)
    color = db.Column(db.Text)

    def __repr__(self):
        return [self.name, self.id, self.info, self.price, self.date, self.image, self.shortname, self.color]


@app.route('/')
@app.route('/main')
def index():
    goods = Goods().query.order_by(Goods.price).all()
    return render_template("index.html", data=goods)


@app.route('/katalog')
def katalog():
    return render_template("katalog.html")


@app.route('/info')
def info():
    return render_template("info.html")


@app.route('/cart')
def cart():
    return 'Корзина'


@app.route('/goods/<shortname>')
def post(shortname):
    good = Goods().query.filter_by(shortname=shortname).first()
    other_goods = Goods().query.filter(Goods.shortname.startswith(good.shortname.split('_')[0])).all()
    return render_template("index_goods.html", dats=good, other_goods=other_goods)

# @app.route('/<good_name>')
# def show_good_name(good_name):
#     return render_template(f'{good_name}.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        info = request.form['info']
        image = request.files['file']
        print(os.path.join(""))
        image.save(os.path.join('static\\img\\goods', image.filename))

        goods = Goods(name=name, price=price, info=info, image="img/goods/"+str(image.filename))

        try:
            db.session.add(goods)
            db.session.commit()
            return redirect('/')
        except Exception as err:
            print(f"db.create error: {err}")
            return "Ошибка"
    else:
        return render_template("create.html")


# @app.get('/')
# def index():
#     return render_template(index.html)


if __name__ == '__main__':
    app.run(debug=True)
