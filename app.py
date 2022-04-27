from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model): #used to create instance for db updates
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(155), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task ' + str(self.id)

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_data = request.form['content'] #from html form id/name
        new_task = Todo(content=task_data)

        try:
            db.session.add(new_task) #add to db
            db.session.commit() #commit to db
            return redirect('/') #go back to index.html
        except:
            return 'error adding task to the database'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Problem occured deleting that task'

@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST": #when task is updated
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
        except:
            return 'db error'

        return redirect('/')
    else:
        return render_template('update.html', task=task_to_update)

if __name__ == "__main__":
    app.run(debug=True)
