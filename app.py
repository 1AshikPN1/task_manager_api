from flask import Flask, jsonify, request
from extensions import db, jwt
from config import Config
from models import User, Task

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Task Manager API!"})

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "User already exists"}), 400

        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        output = []
        for task in tasks:
            output.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'user_id': task.assigned_user_id
            })
        return jsonify(output)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
