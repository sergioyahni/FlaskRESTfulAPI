from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.String(10), nullable=False)
    isbn = db.Column(db.String(13), nullable=False)

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}', published_date='{self.published_date}', isbn='{self.isbn}')>"


class BookResource(Resource):
    def get(self, book_id=None):
        if book_id:
            book = Book.query.filter_by(id=book_id).first()
            if book:
                return {'id': book.id, 'title': book.title, 'author': book.author,
                        'published_date': book.published_date, 'isbn': book.isbn}, 200
            else:
                return {'error': 'Book not found.'}, 404
        else:
            books = Book.query.all()
            return {'books': [
                {'id': book.id, 'title': book.title, 'author': book.author, 'published_date': book.published_date,
                 'isbn': book.isbn} for book in books]}, 200

    def post(self):
        # book_data = request.get_json() # chatGPT error: line 38 and line 50 TypeError: 'NoneType' object is not subscriptable
        book_data = request.form # fixing the chatGPT error.
        print(book_data)
        book = Book(title=book_data['title'], author=book_data['author'], published_date=book_data['published_date'],
                    isbn=book_data['isbn'])
        db.session.add(book)
        db.session.commit()
        return {'message': 'Book added successfully.', 'id': book.id}, 201

    def put(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if book:
            # book_data = request.get_json() # chatGPT error: TypeError: 'NoneType' object is not subscriptable
            book_data = request.form  # fixing the chatGPT error.
            book.title = book_data.get('title', book.title)
            book.author = book_data.get('author', book.author)
            book.published_date = book_data.get('published_date', book.published_date)
            book.isbn = book_data.get('isbn', book.isbn)
            db.session.commit()
            return {'message': 'Book updated successfully.'}, 200
        else:
            return {'error': 'Book not found.'}, 404

    def delete(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message': 'Book deleted successfully.'}, 200
        else:
            return {'error': 'Book not found.'}, 404


api.add_resource(BookResource, '/books', '/books/<int:book_id>')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
