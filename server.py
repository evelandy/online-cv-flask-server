# from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify #, make_response
# from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from datetime import datetime
from flask_cors import CORS
# from functools import wraps
# import jwt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:CrxMan161821$@localhost/messages'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = MySQL(app)
db = SQLAlchemy(app)
CORS(app)
Bootstrap(app)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(16))
    message = db.Column(db.String(480), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)


@app.route('/api/v1/check', methods=['GET'])
def check_server():
    return jsonify({'message': 'up and running'}), 200


@app.route('/api/v1/message', methods=['GET'])
def see_all_messages():
    message_list = Messages.query.all()

    output = []

    for msg in message_list:
        msg_data = {}
        msg_data['id'] = msg.id
        msg_data['company'] = msg.company
        msg_data['name'] = msg.name
        msg_data['email'] = msg.email
        msg_data['phone'] = msg.phone
        msg_data['message'] = msg.message
        msg_data['created'] = msg.created
        output.append(msg_data)

    return jsonify(output), 200


@app.route('/api/v1/message/<msg_id>', methods=['GET'])
def see_one_message(msg_id):
    msg = Messages.query.filter_by(id=msg_id).first()

    output = []
    msg_data = {}
    msg_data['id'] = msg.id
    msg_data['company'] = msg.company
    msg_data['name'] = msg.name
    msg_data['email'] = msg.email
    msg_data['phone'] = msg.phone
    msg_data['message'] = msg.message
    msg_data['created'] = msg.created
    output.append(msg_data)

    return jsonify(output), 200



@app.route('/api/v1/message', methods=['POST'])
def add_message():
    data = request.get_json()

    new_msg = Messages(company=data['company'], name=data['name'], email=data['email'],
                       phone=data['phone'], message=data['message'])

    db.session.add(new_msg)
    db.session.commit()

    return jsonify({'message': 'message sent!'}), 200


# @app.route('/api/v1/edit_msg/<msg_id>', methods=['PUT'])
# def edit_message(msg_id):
#     pass


@app.route('/api/v1/del_msg/<msg_id>', methods=['DELETE'])
def remove_message(msg_id):
    msg = Messages.query.filter_by(id=msg_id).first()

    if not msg:
        return jsonify({'message': 'that message does not exist'}), 404

    db.session.delete(msg)
    db.session.commit()

    return jsonify({'message': 'message removed successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
