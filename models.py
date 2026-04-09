from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    __tablename__ = "data"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    URL = db.Column(db.String(255), nullable=False)


class Users(db.Model):
    __tablename__ = "users"
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AADHAR_NUMBER = db.Column(db.String(12), primary_key=True)  # Aadhaar is 12-digit, better as string
    EMAIL = db.Column(db.String(120), unique=True, nullable=False)
    PHONE_NUMBER = db.Column(db.String(15), nullable=False)  # keep as string (handles +91 etc.)
    PASSWORD = db.Column(db.String(255), nullable=False)

    