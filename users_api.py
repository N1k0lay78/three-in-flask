from datetime import datetime

import flask
from flask import jsonify, request

from data import db_session
from data.users import User

blueprint = flask.Blueprint('users_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/users/')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()
    return jsonify(
        {
            'users':
                [user.to_dict(only=(
                    'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))
                    for user in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_one_users(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': user.to_dict(only=(
                'id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))

        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    user = session.query(User).get(request.json['id'])
    if user:
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email']
    )
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    session.delete(users)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def put_users(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    if request.json.get('surname'):
        users.surname = request.json.get('surname')
    if request.json.get('name'):
        users.name = request.json.get('name')
    if request.json.get('age'):
        users.age = request.json.get('age')
    if request.json.get('position'):
        users.position = request.json.get('position')
    if request.json.get('speciality'):
        users.speciality = request.json.get('speciality')
    if request.json.get('address'):
        users.address = request.json.get('address')
    if request.json.get('email'):
        users.email = request.json.get('email')
    session.commit()
    return jsonify({'success': 'OK'})