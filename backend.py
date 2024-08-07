from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
from flask_cors import CORS
app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Karsah_2104'
app.config['MYSQL_DB'] = 'bookstore'
app.config['PORT'] = '3306'

mysql = MySQL(app)

CORS(app)

@app.route('/users', methods=['GET'])
def login():
    try:
        email = request.args.get('email')
        password = request.args.get('password')
        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM users WHERE UserEmail = %s"
        val = (email,)
        mycursor.execute(sql,val)
        response = mycursor.fetchone()


        if(password == response[3]) :
            return jsonify({'status': 'Login Successful','id' : response[0],'name' : response[1],'library': response[5],'type' : response[4]}),200
        else:
            return jsonify('Login Failed'), 400

    except Exception as e:
        return jsonify('An error has occured'),500

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if data is None:
            return jsonify('No data provided'), 400

        email = request.json['email']
        password = request.json['password']
        name = request.json['name']
        type = request.json['type']

        if not email or not password:
            return jsonify('Missing required fields'), 400

        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM users WHERE UserEmail = %s"
        val = (email,)
        mycursor.execute(sql, val)
        if mycursor.fetchone():
            return jsonify('Email already exists'), 400



        sql = "INSERT INTO users (UserEmail, UserPassword,UserName,UserType) VALUES (%s, %s,%s,%s)"
        val = (email,password,name,type)
        mycursor.execute(sql, val)
        mysql.connection.commit()
        return jsonify('User created successfully'), 201

    except Exception as e:
        return jsonify('An error has occured'),500

@app.route('/library', methods=['GET'])
def get_libraries():
    try:
        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM library"
        mycursor.execute(sql)
        response = mycursor.fetchall()
        return jsonify(response), 400
    except Exception as e:
        return jsonify('An error has occured'),500

@app.route('/library/location', methods=['GET'])
def get_libraries_location():
    try:
        location = request.args.get('location')
        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM library WHERE LibraryLocation = %s"
        val = (location,)
        mycursor.execute(sql,val)
        response = mycursor.fetchall()
        return jsonify(response), 400
    except Exception as e:
        return jsonify('An error has occured'),500

@app.route('/books', methods=['POST'])
def add_book():
    try:
        mycursor = mysql.connection.cursor()
        data = request.get_json()
        if data is None:
            return jsonify('No data provided'), 400

        title = request.json['title']
        author = request.json['author']
        description = request.json['description']
        price = request.json['price']
        genre = request.json['genre']
        library = request.json['library']
        url = request.json['url']


        sql = "INSERT INTO books (BookTitle,BookAuthor,BookDescription,BookPrice,Genre,LibraryBook,ImageURL) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (title,author,description,price,genre,library,url,)
        mycursor.execute(sql, val)
        mysql.connection.commit()
        return jsonify('Book added successfully'), 201

    except Exception as e:
        return jsonify('An error has occured'),500

@app.route('/books' , methods = ['DELETE'])
def delete_book():
    try:
        id = request.args.get('id')
        mycursor = mysql.connection.cursor()
        sql = "DELETE FROM books WHERE BookID = %s"
        val = (id,)
        mycursor.execute(sql,val)
        mysql.connection.commit()
        return jsonify('Book deleted Successfully'), 400
    except Exception as e:
        return jsonify('An error has occured'),500


@app.route('/books', methods=['GET'])
def get_all_books():
    try:
        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM books"
        mycursor.execute(sql)
        response = mycursor.fetchall()
        return jsonify(response), 200
    except Exception as e:
        return jsonify('An error has occured'),500

@app.route('/books/lib', methods=['GET'])
def get_books_library():
    try:
        id = request.args.get('id')
        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM books WHERE LibraryBook = %s"
        val = (id,)
        mycursor.execute(sql,id)
        response = mycursor.fetchall()
        return jsonify(response), 400
    except Exception as e:
        return jsonify('An error has occured'),500




if __name__ == '__main__':
    app.run(debug=True)
