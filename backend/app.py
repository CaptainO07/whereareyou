from flask import Flask, jsonify,render_template,redirect,url_for,request,session
from models import *
from flask_sqlalchemy import SQLAlchemy

import os
from werkzeug.utils import secure_filename
app=Flask(__name__)
app.config['SECRET_KEY']='super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres.hrbjruqitvtxwponfuii:PLaC8uLUE7qRbtCe@aws-1-ap-south-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/",methods=["POST","GET"])
def root():
    if request.method=="POST":
        return redirect(url_for('check'))
    else:
        return render_template('home.html')

@app.route("/check",methods=["POST","GET"])
def check():
    if(request.method=="POST"):
        email=request.form.get("Email")
        url=request.form.get("Url")
        screenshot=request.files.get("Image")
        screenshot.save(os.path.join('uploads',secure_filename(screenshot.filename)))
        print(email)
        print(url)
        print(screenshot)
    return render_template('welcome.html')

@app.route("/submiturl",methods=["GET","POST"])
def submiturl():
    if request.method=="POST":
        data:dict=request.get_json()
        Url=data.get("url")
        info=Data(URL=Url)
        db.session.add(info)
        db.session.commit()
    return render_template('submiturl.html')

@app.route("/phishurls",methods=["GET","POST"])
def see_url():
    if request.method=="GET":
        info=Data.query.all()
        return jsonify(info)
@app.route("/see_url")
def random():
    return render_template('see_url.html')
@app.route("/register",methods=["GET","POST"])
def registration():
    if(request.method=="POST"):
        data:dict=request.get_json()
        Aadhar_number=data.get("aadhaar_number")
        Email=data.get("email")
        Phone_number=data.get("phone_number")
        Password=data.get("password")
        info=Users(AADHAR_NUMBER=Aadhar_number,EMAIL=Email,PHONE_NUMBER=Phone_number,PASSWORD=Password)
        db.session.add(info)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        data:dict=request.get_json()
        Email=data.get("email")
        Password=data.get("password")
        info=Users.query.filter_by(EMAIL=Email).first()
        if(info.PASSWORD==Password):
            session["email"]=info.EMAIL
            return redirect(url_for('welcome'))
        elif(info.EMAIL!=Email):
            return "email is not registered",400
        else:
            return "wrong password",404
    
    return render_template('login.html')


if __name__=='__main__':
    app.run(debug=True,threaded=True)
