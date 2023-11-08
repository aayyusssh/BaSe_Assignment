from . import auth
from flask import request, jsonify, session
from ..models import db, User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        get_data = request.get_json()
        username = get_data["username"]
        password = get_data["password"]
        email = get_data["email"]
        is_admin = get_data["is_admin"]

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()

        if existing_user:
            response = {'message': 'Username or email already exists. Please choose a different one.'}
            return jsonify(response), 400
        else:
            # If the username or email is not taken, create a new user and add it to the database
            user = User(username=username, password=password, email=email,is_admin=is_admin)
            db.session.add(user)
            db.session.commit()
            response = {'message': 'Registration successful. You can now log in.'}
            return jsonify(response), 200

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        #check if an user is already logged in
        if 'user_id' in session:
            return jsonify({"message":"A user is already loggedin, log out first"})
        get_data = request.get_json()
        username = get_data["username"]
        password = get_data["password"]
        user = User.query.filter_by(username=username).first()

        
        if user and user.password == password:
            session['user_id'] = user.id
            response = {'message': 'Login Successfull'}
            return jsonify(response), 200
        else:
            response = {'message':'Login failed. Please check your credentials.'}
            return jsonify(response), 400

@auth.route('/logout')
def logout():
    if 'user_id' not in session:
        return jsonify({'message': 'already logged out'}), 401
    session.pop('user_id', None)
    response = {'message': 'Logout Successfull'}
    return jsonify(response), 200