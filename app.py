from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        print(request.form['title'])
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allToDo = Todo.query.all()
    return render_template('index.html', allToDo=allToDo)

@app.route('/show')
def products():
    allToDo = Todo.query.all()
    print(allToDo)
    return 'this is products page'

@app.route('/update/<int:Sno>', methods=['GET', 'POST'])
def update(Sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        ToDo = Todo.query.filter_by(Sno=Sno).first()
        ToDo.title = title
        ToDo.desc = desc
        db.session.add(ToDo)
        db.session.commit()
        return redirect("/")
    ToDo = Todo.query.filter_by(Sno=Sno).first()
    return render_template('update.html', ToDo=ToDo)

@app.route('/delete/<int:Sno>')
def delete(Sno):
    ToDo = Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(ToDo)
    db.session.commit()
    return redirect("/")

if __name__== "__main__":
    app.run(debug=True)