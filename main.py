from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'anything'

db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), unique=True, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.username

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  else:
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and (password == user.password):
      session['username'] = username
      return redirect('/')
    else:
      return render_template('login.html', message='Invalid username or password')

@app.route('/register', methods=['POST', 'GET'])
def register():
  if request.method == 'GET':
    return render_template('register.html')
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm-password")
    user = User.query.filter_by(username=username).first()
    if user:
      return render_template('register.html', message='Please choose a different username')
    else:
      if password == confirm:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/')
      else:
        return render_template('register.html', message = 'Passwords do not match')

@app.route('/')
def index():
  if 'username' in session:
    return render_template('index.html', username=session['username'])
  else:
    return render_template('register.html')

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect("/")

with app.app_context():
  db.create_all()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
