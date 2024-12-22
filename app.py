from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for Alumni Data
class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    batch = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    percentage = db.Column(db.Float, nullable=False)
    current_status = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/')
def index():
    alumni = Alumni.query.all()
    return render_template('index.html', alumni=alumni)

@app.route('/add', methods=['GET', 'POST'])
def add_alumni():
    if request.method == 'POST':
        name = request.form['name']
        batch = request.form['batch']
        department = request.form['department']
        email = request.form['email']
        phone = request.form['phone']
        percentage = request.form['percentage']
        current_status = request.form['current_status']

        new_alumni = Alumni(name=name, batch=batch, department=department, email=email, phone=phone,
                            percentage=percentage, current_status=current_status)
        db.session.add(new_alumni)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_alumni(id):
    alumni = Alumni.query.get_or_404(id)
    if request.method == 'POST':
        alumni.name = request.form['name']
        alumni.batch = request.form['batch']
        alumni.department = request.form['department']
        alumni.email = request.form['email']
        alumni.phone = request.form['phone']
        alumni.percentage = request.form['percentage']
        alumni.current_status = request.form['current_status']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update.html', alumni=alumni)

@app.route('/delete/<int:id>')
def delete_alumni(id):
    alumni = Alumni.query.get_or_404(id)
    db.session.delete(alumni)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_alumni():
    if request.method == 'POST':
        search_term = request.form['search']
        results = Alumni.query.filter(
            Alumni.name.like(f"%{search_term}%") |
            Alumni.batch.like(f"%{search_term}%") |
            Alumni.department.like(f"%{search_term}%") |
            Alumni.current_status.like(f"%{search_term}%")
        ).all()
        return render_template('search.html', alumni=results, search_term=search_term)

    return render_template('search.html', alumni=None, search_term=None)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
