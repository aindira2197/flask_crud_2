from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':
        task = request.form.get('task')

        todo = Todo(task=task)

        db.session.add(todo)
        db.session.commit()

        return redirect('/')

    return render_template('create.html')


@app.route('/complete/<int:id>')
def complete(id):

    todo = Todo.query.get(id)

    todo.completed = True

    db.session.commit()

    return redirect('/')


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
