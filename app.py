from flask import Flask, jsonify,render_template,redirect,url_for,request,session, send_from_directory, session 
from models import *
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_env
import os
from werkzeug.utils import secure_filename
app=Flask(__name__)

from dotenv import load_dotenv
load_dotenv()

app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('SQLURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)
tmp='templates'
with app.app_context():
    db.create_all()

@app.route("/",methods=["POST","GET"])
def root():
    if 'user' not in session :
        return redirect(url_for('login'))

    if request.method=="POST":
        return redirect(url_for('check'))
    else:
        return send_from_directory('templates','home.html')

@app.route("/check",methods=["POST","GET"])
def check():
    if 'user' not in session :
        return redirect(url_for('login'))
    if(request.method=="POST"):
        email=request.form.get("Email")
        url=request.form.get("Url")
        screenshot=request.files.get("Image")
        screenshot.save(os.path.join('uploads',secure_filename(screenshot.filename)))
        print(email)
        print(url)
        print(screenshot)
    return send_from_directory('templates','check.html')

@app.route("/submiturl",methods=["GET","POST"])
def submiturl():
    if 'user' not in session :
        return redirect(url_for('login'))
    if request.method=="POST":
        data:dict=request.get_json()
        Url=data.get("url")
        info=Data(URL=Url)
        db.session.add(info)
        db.session.commit()
    return render_template('submiturl.html')

@app.route("/phishurls",methods=["GET","POST"])
def see_url():
    if 'user' not in session :
        return redirect(url_for('login'))
    if request.method=="GET":
        info=Data.query.all()
        return jsonify(info)
@app.route("/see_url")
def random():
    if 'user' not in session :
        return redirect(url_for('login'))
    return render_template('see_url.html')
@app.route("/register",methods=["GET","POST"])
def registration():
    if 'user' in session:
        return redirect(url_for('root'))
    if(request.method=="POST"):
        
        data:dict=request.get_json()
        Aadhar_number=data.get("aadhaar_number")
        Email=data.get("email")
        Phone_number=data.get("phone_number")
        Password=data.get("password")
        info=Users(AADHAR_NUMBER=Aadhar_number,EMAIL=Email,PHONE_NUMBER=Phone_number,PASSWORD=Password)
        db.session.add(info)
        db.session.commit()
        return jsonify(msg="go and login"),200 

    return send_from_directory(tmp,'register.html')



@app.route("/login",methods=["GET","POST"])
def login():
    if 'user' in session:
        return redirect(url_for('root'))
    if(request.method=="POST"):
        data:dict=request.get_json()
        Email=data.get("email")
        print(Email)
        Password=data.get("password")
        print(Password)
        info=Users.query.filter_by(EMAIL=Email).first()
        if(info.PASSWORD==Password):
            session["user"]=info.EMAIL
            return jsonify(msg="correct password"),200
        elif(info.EMAIL!=Email):
            return jsonify(msg="email is not registered"),400
        else:
            return jsonify(msg="wrong password"),404
     
    

    return send_from_directory(tmp,'login.html')

@app.route('/clearsession')
def clear_session():
    session.clear()
    return redirect(url_for('login'))



if __name__=='__main__':
    app.run(debug=True,threaded=True)