from flask import Flask,render_template,session,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house_rental.db'
app.secret_key = "super-secret-key"
db=SQLAlchemy(app)

class categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class houses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_no = db.Column(db.String(80),unique=True, nullable=False)
    category_id = db.Column(db.String(80),unique=False, nullable=False)
    description = db.Column(db.String(80),unique=False, nullable=False)
    price = db.Column(db.Integer,unique=False,nullable=False)
    
class tenants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    contact = db.Column(db.String(12), unique=False, nullable=False)
    house_id = db.Column(db.String(12), unique=False, nullable=False)
    date_in = db.Column(db.String(6), unique=False, nullable=False)

@app.route("/",methods=['GET','POST'])
@app.route("/dashboard",methods=['GET','POST'])
def login():
    if 'user' in session and session['user'] == params['uname']:
        if request.method == 'POST':
            name = request.form.get('name')
            entry = categories(name=name)
            db.session.add(entry)
            db.session.commit()
            return redirect("/")
        data = categories.query.all()
        return render_template("dashboard.html",params=params,data=data)

    if request.method == 'POST':
        uname = request.form.get('uname')
        password = request.form.get('pass')
        if(uname == params['uname'] and password == params['pass']):
            session['user'] = uname
            return redirect("/")
            if request.method == 'POST':
                name = request.form.get('name')
                entry = categories(name=name)
                db.session.add(entry)
                db.session.commit()
                return redirect("/")
            data = categories.query.all()
            return render_template("dashboard.html",params=params,data=data)   
        else:
            return "your user name and password should be a wrong."
    else:
        return render_template("login.html",params=params)

@app.route("/edit/<string:id>",methods=['GET','POST'])
def edit(id):
    if 'user' in session and session['user'] == params['uname']:
        if request.method == "POST":
            name = request.form.get('name')
            data = categories.query.filter_by(id=id).first()
            data.name = name
            db.session.commit()
        data = categories.query.filter_by(id=id).first()
        return render_template("edit.html",data=data)


@app.route('/delete/<string:id>',methods = ['GET','POST'])
def delete(id):
	if 'user' in session and session['user'] == params['uname']:
		posts = categories.query.filter_by(id=id).first()
		db.session.delete(posts)
		db.session.commit()
	return redirect('/dashboard')



@app.route("/house")
def house():
    if 'user' in session and session['user'] == params['uname']:
        data = houses.query.all()
        return render_template("house.html",data=data)

@app.route("/house_new",methods=['GET','POST'])
def house_new():
    if 'user' in session and session['user'] == params['uname']:
        data = categories.query.all()
        if request.method == "POST":
            house_no = request.form.get('house_no')
            category_id = request.form.get('category_id')
            description = request.form.get('description')
            price = request.form.get('price')
            entry = houses(house_no=house_no ,category_id=category_id,description=description,price=price)
            db.session.add(entry)
            db.session.commit()
        return render_template("house_new.html",data=data)

@app.route("/edit_house/<string:id>",methods=['GET',"POST"])
def edit_house(id):
    if 'user' in session and session['user'] == params['uname']:
        if request.method == "POST":
            house_no = request.form.get('house_no')
            category_id = request.form.get('category_id')
            description = request.form.get('description')
            price = request.form.get('price')
            data = houses.query.filter_by(id=id).first()
            data.house_new=house_new
            data.category_id=category_id
            data.description=description
            data.price=price
            db.session.commit()
        data = houses.query.filter_by(id=id).first()
        data1 = categories.query.all()
        return render_template("edit_house.html",data=data,data1=data1)
        
@app.route('/delete_house/<string:id>',methods = ['GET','POST'])
def delete_house(id):
	if 'user' in session and session['user'] == params['uname']:
		posts = houses.query.filter_by(id=id).first()
		db.session.delete(posts)
		db.session.commit()
	return redirect('/house')

@app.route("/tenant")
def tenant():
    if 'user' in session and session['user'] == params['uname']:
        data = tenants.query.all()
        return render_template("tenant.html",data=data)

@app.route("/new_tenant",methods=['GET','POST'])
def new_tenant():
    if 'user' in session and session['user'] == params['uname']:
        if request.method == "POST":
            name = request.form.get('name')
            email = request.form.get('email')
            contact = request.form.get('contact')
            house_id = request.form.get('house_id')
            entry = tenants(name=name,email=email,contact=contact,house_id=house_id,date_in=date.today())
            db.session.add(entry)
            db.session.commit()
        return render_template("new_tenant.html")

@app.route("/edit_tenant/<string:id>",methods=['GET','POST'])
def edit_tenant(id):
    if 'user' in session and session['user'] == params['uname']:
        if request.method == "POST":
            name = request.form.get('name')
            email = request.form.get('email')
            contact = request.form.get('contact')
            house_id = request.form.get('house_id')
            data = tenants.query.filter_by(id=id).first()
            data.name =name
            data.email =email
            data.contact=contact
            data.house_id=house_id
            db.session.commit()
        data = tenants.query.filter_by(id=id).first()
        return render_template("edit_tenant.html",data=data)

@app.route('/delete_tenant/<string:id>',methods = ['GET','POST'])
def delete_tenant(id):
	if 'user' in session and session['user'] == params['uname']:
		posts = tenants.query.filter_by(id=id).first()
		db.session.delete(posts)
		db.session.commit()
	return redirect('/tenant')


@app.route('/logout')
def logout():
	session.pop('user')
	return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)