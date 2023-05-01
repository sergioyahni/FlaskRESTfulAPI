from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, Model
from datetime import datetime

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///products.db'
db = SQLAlchemy(app)


class ProductModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)


# db.create_all()

product_post_args = reqparse.RequestParser()
product_post_args.add_argument("name", type=str, help="Name of the video is required.", required=True)
product_post_args.add_argument("description", type=str, help="Short description of the product is required.",
                               required=True)
product_post_args.add_argument("price", type=float, help="price of the product is required.", required=True)

product_patch_args = reqparse.RequestParser()
product_patch_args.add_argument("name", type=str, help="Name of the video is required.")
product_patch_args.add_argument("description", type=str, help="Short description of the product is required.")
product_patch_args.add_argument("price", type=float, help="price of the product is required.")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "date_created": fields.DateTime,
    "date_updated": fields.DateTime
}


class Product(Resource):
    @marshal_with(resource_fields)
    def get(self, pid=None):
        if pid:
            product = ProductModel.query.filter_by(id=pid).first()
            if not product:
                abort(404, message="Product does not exist.")
            return product
        else:
            product = ProductModel.query.all()
            return product, 200

    @marshal_with(resource_fields)
    def post(self):
        pid = datetime.now().strftime("%m%d%H%M%S%f")
        date_created = datetime.now()
        args = product_post_args.parse_args()
        product = ProductModel(id=pid,
                               name=args["name"],
                               description=args["description"],
                               price=args["price"],
                               date_created=date_created,
                               date_updated=date_created)
        db.session.add(product)
        db.session.commit()
        return product, 201

    @marshal_with(resource_fields)
    def patch(self, pid):
        date_updated = datetime.now()
        args = product_patch_args.parse_args()
        product = ProductModel.query.filter_by(id=pid).first()
        if not product:
            abort(404, message="Video does not exist.")
        product.name = args["name"] if args["name"] else product.name
        product.description = args["description"] if args["description"] else product.description
        product.price = args["price"] if args["price"] else product.price
        product.date_created = product.date_created
        product.date_updated = date_updated
        db.session.commit()
        return product, 201

    def delete(self, pid):
        product = ProductModel.query.filter_by(id=pid).first()
        if not product:
            abort(404, message="Video does not exist.")
        db.session.delete(product)
        db.session.commit()
        return {"deleted": f"{product.name}(pid: {pid})"}, 200


# api.add_resource(AllProducts, "/products")
api.add_resource(Product, "/product", "/product/<int:pid>")

if __name__ == "__main__":
    app.run(debug=True)
